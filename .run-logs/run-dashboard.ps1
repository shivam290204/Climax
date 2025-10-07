Set-Location 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\policy-dashboard'
if (Test-Path 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\.venv\Scripts\activate.ps1') { . 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\.venv\Scripts\activate.ps1' }
if (Test-Path .venv\Scripts\activate.ps1) { . .venv\Scripts\activate.ps1 }
# Load .env from root once per process
if (Test-Path 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform/.env') {
  Get-Content 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform/.env' | Where-Object {  -match '^[A-Za-z_][A-Za-z0-9_]*=' } | ForEach-Object {
     =  -split '=',2; =[0]; =[1]; if (.StartsWith('"') -and .EndsWith('"')) {  = .Substring(1,.Length-2) }
    if () { Set-Item -Path "Env:" -Value  }
  }
}
Write-Host '[service:dashboard] npm run dev' -ForegroundColor DarkGray
Invoke-Expression "npm run dev" *>&1 | Tee-Object -FilePath 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\.run-logs\dashboard.log'
