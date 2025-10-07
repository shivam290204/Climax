<#!
.SYNOPSIS
  Stop all processes started by run-all.ps1.
.DESCRIPTION
  Reads .run-pids.json and attempts to gracefully then forcibly terminate each PID.
#>
param()
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile = Join-Path $Root '.run-pids.json'
if (-not (Test-Path $PidFile)) { Write-Host 'No PID file found.' -ForegroundColor Yellow; exit 0 }
$items = Get-Content $PidFile | ConvertFrom-Json
foreach ($p in $items) {
  try {
    $proc = Get-Process -Id $p.pid -ErrorAction Stop
    Write-Host "Stopping $($p.name) (PID $($p.pid))" -ForegroundColor Cyan
    $proc.CloseMainWindow() | Out-Null
    Start-Sleep -Milliseconds 400
    if (-not $proc.HasExited) { $proc | Stop-Process -Force }
  } catch {
    Write-Host "Already stopped: $($p.name) (PID $($p.pid))" -ForegroundColor DarkGray
  }
}
Remove-Item $PidFile -ErrorAction SilentlyContinue
Write-Host 'All processes terminated.' -ForegroundColor Green
