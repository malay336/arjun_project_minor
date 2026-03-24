# PowerShell script to register the bundled Qwen model with Ollama on a new computer
$ErrorActionPreference = "Stop"

$sourceDir = Join-Path $PSScriptRoot "models\ollama"
$targetDir = Join-Path $env:USERPROFILE ".ollama\models"

if (-not (Test-Path $sourceDir)) {
    Write-Host "Error: Bundled model folder 'models\ollama' not found!" -ForegroundColor Red
    exit 1
}

Write-Host "--- Offline AI Assistant: Importing LLM Model ---" -ForegroundColor Cyan

# 1. Create target directories
$targetBlobs = Join-Path $targetDir "blobs"
$targetManifests = Join-Path $targetDir "manifests\registry.ollama.ai\library\qwen2.5"

if (-not (Test-Path $targetBlobs)) { New-Item -ItemType Directory -Path $targetBlobs -Force | Out-Null }
if (-not (Test-Path $targetManifests)) { New-Item -ItemType Directory -Path $targetManifests -Force | Out-Null }

# 2. Copy Blobs
Write-Host "Copying model blobs to $targetBlobs..."
Copy-Item -Path (Join-Path $sourceDir "blobs\*") -Destination $targetBlobs -Force -ErrorAction SilentlyContinue

# 3. Copy Manifest
Write-Host "Registering model manifest..."
Copy-Item -Path (Join-Path $sourceDir "manifests\registry.ollama.ai\library\qwen2.5\0.5b") -Destination $targetManifests -Force

Write-Host "`nSuccess! The qwen2.5:0.5b model is now registered with Ollama." -ForegroundColor Green
Write-Host "You can now run 'ollama list' to verify, or start the assistant using 'run.bat'." -ForegroundColor Yellow
pause
