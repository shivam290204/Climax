<#!
.SYNOPSIS
  Launch backend (FastAPI), optional repeating data pipeline, policy dashboard (Vite), and optionally Expo (mobile/web) concurrently.
.DESCRIPTION
  Spawns each service in its own PowerShell child process, captures PIDs to .run-pids.json and logs output to .run-logs/*.log.
.PARAMETER NoMobile
  Skip starting the Expo dev server.
.PARAMETER PipelineLoop
  Re-run the data pipeline runner.py on an interval (seconds) instead of once.
.PARAMETER PipelineIntervalSeconds
  Interval (default 900 seconds) between pipeline runs when -PipelineLoop is used.
.PARAMETER ClearExpo
  Pass --clear to Expo start (forces Metro cache clear).
.EXAMPLE
  ./run-all.ps1 -NoMobile
.EXAMPLE
  ./run-all.ps1 -PipelineLoop -PipelineIntervalSeconds 600
.NOTES
  Stop everything with ./stop-all.ps1
#>
param(
  [switch]$NoMobile,
  [switch]$PipelineLoop,
  [int]$PipelineIntervalSeconds = 900,
  [switch]$ClearExpo
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$LogDir = Join-Path $Root '.run-logs'
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$PidFile = Join-Path $Root '.run-pids.json'
$Procs = @()

function Start-ServiceProc {
  param(
    [Parameter(Mandatory)][string]$Name,
    [Parameter(Mandatory)][string]$Command,
    [Parameter(Mandatory)][string]$WorkingDir,
    [string]$LogFile
  )
  Write-Host "Starting $Name ..." -ForegroundColor Cyan
  $logPath = if ($LogFile) { Join-Path $LogDir $LogFile } else { Join-Path $LogDir ("$Name.log") }
  $rootVenvActivate = Join-Path $Root '.venv/Scripts/activate.ps1'
  $wrapper = @"
Set-Location '$WorkingDir'
if (Test-Path '$rootVenvActivate') { . '$rootVenvActivate' }
if (Test-Path .venv\Scripts\activate.ps1) { . .venv\Scripts\activate.ps1 }
# Load .env from root once per process
if (Test-Path '$Root/.env') {
  Get-Content '$Root/.env' | Where-Object { $_ -match '^[A-Za-z_][A-Za-z0-9_]*=' } | ForEach-Object {
    $kv = $_ -split '=',2; $k=$kv[0]; $v=$kv[1]; if ($v.StartsWith('"') -and $v.EndsWith('"')) { $v = $v.Substring(1,$v.Length-2) }
    if ($k) { Set-Item -Path "Env:$k" -Value $v }
  }
}
Write-Host '[service:$Name] $Command' -ForegroundColor DarkGray
Invoke-Expression "$Command" *>&1 | Tee-Object -FilePath '$logPath'
"@
  $wrapperPath = Join-Path $LogDir ("run-" + $Name + ".ps1")
  $wrapper | Out-File -FilePath $wrapperPath -Encoding UTF8
  $p = Start-Process -FilePath "powershell.exe" -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File', $wrapperPath -PassThru -WindowStyle Minimized
  $script:Procs += [pscustomobject]@{ name = $Name; pid = $p.Id; log = $logPath; script = $wrapperPath }
}

# Backend
$backendDir = Join-Path $Root 'backend'
Start-ServiceProc -Name 'backend' -WorkingDir $backendDir -Command "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Data pipeline (single run or loop)
$pipelineDir = Join-Path $Root 'data-pipeline'
if ($PipelineLoop) {
  $loopWrapper = @"
Set-Location '$pipelineDir'
if (Test-Path .venv\Scripts\activate.ps1) { . .venv\Scripts\activate.ps1 }
Write-Host '[pipeline] loop starting interval=$PipelineIntervalSeconds' -ForegroundColor Yellow
while ($true) {
  try {
    $env:OPENAQ_BASE = 'https://api.openaq.org/v2'
    python runner.py
  } catch { Write-Host ('[pipeline] error: ' + $_) -ForegroundColor Red }
  Start-Sleep -Seconds $PipelineIntervalSeconds
}
"@
  $loopPath = Join-Path $LogDir 'pipeline-loop.ps1'
  $loopWrapper | Out-File -FilePath $loopPath -Encoding UTF8
  Start-ServiceProc -Name 'pipeline-loop' -WorkingDir $pipelineDir -Command "powershell -NoProfile -ExecutionPolicy Bypass -File `"$loopPath`""
} else {
  Start-ServiceProc -Name 'pipeline-once' -WorkingDir $pipelineDir -Command "python runner.py"
}

# Policy dashboard (Vite)
$dashboardDir = Join-Path $Root 'policy-dashboard'
Start-ServiceProc -Name 'dashboard' -WorkingDir $dashboardDir -Command "npm run dev"

# Mobile (Expo) unless skipped
if (-not $NoMobile) {
  $mobileDir = Join-Path $Root 'mobile-app'
  $expoArgs = if ($ClearExpo) { 'start --clear' } else { 'start' }
  Start-ServiceProc -Name 'expo' -WorkingDir $mobileDir -Command "npx expo $expoArgs"
}

# Persist PIDs
$Procs | ConvertTo-Json | Out-File -Encoding UTF8 $PidFile
Write-Host "Saved process info to $PidFile" -ForegroundColor Green

# Wait for backend health (simple readiness probe)
$healthUrl = 'http://127.0.0.1:8000/health'
$deadline = (Get-Date).AddSeconds(45)
Write-Host 'Waiting for backend health...' -NoNewline
while ((Get-Date) -lt $deadline) {
  try {
    $r = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 3
    if ($r.status -eq 'ok') { Write-Host " OK" -ForegroundColor Green; break }
  } catch { Start-Sleep -Milliseconds 800 }
  Write-Host '.' -NoNewline
}

if ((Get-Date) -ge $deadline) {
  Write-Host " backend not healthy within timeout" -ForegroundColor Yellow
  $backendLog = Join-Path $LogDir 'backend.log'
  if (Test-Path $backendLog) {
    Write-Host '--- backend.log (last 40 lines) ---' -ForegroundColor DarkYellow
    Get-Content $backendLog -Tail 40 | ForEach-Object { Write-Host $_ }
  } else {
    Write-Host 'No backend log produced. Possible causes: python not found, virtual env not activated, uvicorn not installed.' -ForegroundColor Red
  }
}

Write-Host "Services started:" -ForegroundColor Cyan
$Procs | ForEach-Object { Write-Host (" - {0} (PID {1}) -> {2}" -f $_.name, $_.pid, $_.log) }

Write-Host "To stop: ./stop-all.ps1" -ForegroundColor Magenta
