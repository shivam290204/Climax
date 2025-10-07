Set-Location 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\backend'
if (Test-Path 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\.venv\Scripts\activate.ps1') { . 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\.venv\Scripts\activate.ps1' }
if (Test-Path .venv\Scripts\activate.ps1) { . .venv\Scripts\activate.ps1 }
# Load .env from root once per process
if (Test-Path 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform/.env') {
  Get-Content 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform/.env' | Where-Object {  -match '^[A-Za-z_][A-Za-z0-9_]*=' } | ForEach-Object {
     =  -split '=',2; =[0]; =[1]; if (.StartsWith('"') -and .EndsWith('"')) {  = .Substring(1,.Length-2) }
    if () { Set-Item -Path "Env:" -Value  }
  }
}
Write-Host '[service:backend] python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload' -ForegroundColor DarkGray
Invoke-Expression "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload" *>&1 | Tee-Object -FilePath 'C:\Users\DELL\OneDrive - hmritm.ac.in\Desktop\Codes\New folder (2)\delhi-ncr-pollution-platform\.run-logs\backend.log'
