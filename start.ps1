$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $projectRoot "frontend"
$backendPath = Join-Path $projectRoot "backend"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    $nodePath = "C:\Program Files\nodejs"
    if (Test-Path (Join-Path $nodePath "node.exe")) {
        $env:Path = "$nodePath;$env:Path"
    }
}

if (-not (Get-Command node -ErrorAction SilentlyContinue) -or -not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "Node.js and npm are required. Install Node.js from https://nodejs.org/, reopen PowerShell, then run .\start.ps1 again."
}

Push-Location $frontendPath
try {
    if (-not (Test-Path "node_modules")) {
        npm install
    }
    npm run build
}
finally {
    Pop-Location
}

$python = Join-Path $backendPath "venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

Push-Location $backendPath
try {
    & $python -m pip install -r requirements.txt
}
finally {
    Pop-Location
}

Start-Process -FilePath $python -WorkingDirectory $backendPath -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000")
Start-Process "http://localhost:8000"
Write-Host "MPLADS Sentinel AI is starting at http://localhost:8000"
