# run_demo.ps1 - convenience script to run i1 demo server and demo client
$cwd = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Join-Path $cwd "..\Jarvis-Vector-COS\i1"
Set-Location $project
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment and installing dependencies..."
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install --upgrade pip
    pip install -r requirements.txt
} else {
    .\.venv\Scripts\Activate.ps1
}
Start-Process -NoNewWindow -FilePath python -ArgumentList "api_server.py"
Start-Sleep -Seconds 2
python demo.py
