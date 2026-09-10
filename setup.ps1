# ==========================================================
# VISTOR Project Setup
#
# Official Bootstrap Installer
#
# Version      : 1.0
# Project      : VISTOR
# Author       : Colin Rosenthal
# Last Updated : July 2026
#
# Description:
# Creates the VISTOR project structure.
# Safe to run multiple times.
# Never overwrites existing work.
#
# ==========================================================
$ErrorActionPreference = "Stop"

$ProjectRoot = $PSScriptRoot

$FoldersCreated = 0
$FoldersSkipped = 0

$FilesCreated = 0
$FilesSkipped = 0

$Errors = 0

function Write-Section {
    param([string]$Title)

    Write-Host ""
    Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host $Title -ForegroundColor Cyan
    Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray
}

function Write-Success {
    param([string]$Message)

    Write-Host "[+] $Message" -ForegroundColor Green
}

function Write-Skip {
    param([string]$Message)

    Write-Host "[=] $Message" -ForegroundColor DarkGray
}

function Write-ErrorMessage {
    param([string]$Message)

    Write-Host "[!] $Message" -ForegroundColor Red
}

function New-VistorFolder {

    param([string]$RelativePath)

    $FullPath = Join-Path $ProjectRoot $RelativePath

    if (Test-Path $FullPath) {

        $script:FoldersSkipped++

        Write-Skip $RelativePath

    }
    else {

        New-Item `
            -ItemType Directory `
            -Path $FullPath `
            -Force | Out-Null

        $script:FoldersCreated++

        Write-Success $RelativePath

    }

}

function New-VistorFile {

    param([string]$RelativePath)

    $FullPath = Join-Path $ProjectRoot $RelativePath

    if (Test-Path $FullPath) {

        $script:FilesSkipped++

        Write-Skip $RelativePath

    }
    else {

        New-Item `
            -ItemType File `
            -Path $FullPath `
            -Force | Out-Null

        $script:FilesCreated++

        Write-Success $RelativePath

    }

}

Clear-Host

Write-Host "============================================================" -ForegroundColor DarkCyan
Write-Host "                 VISTOR Project Setup" -ForegroundColor Cyan
Write-Host "                        Version 1.0" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor DarkCyan

Write-Host ""
Write-Host "Project Root:" -ForegroundColor Yellow
Write-Host "  $ProjectRoot"

# ==========================================================
# Project Structure
# ==========================================================

$Folders = @(
    "Assets",
    "Assets\Backgrounds",
    "Assets\Fonts",
    "Assets\Icons",
    "Assets\Logos",
    "Assets\OSD",
    "Assets\Sounds",
    "Assets\Weather",

    "Cache",

    "ChannelConfigs",

    "src",
    "src\channel",
    "src\core",
    "src\engine",
    "src\guide",
    "src\metadata",
    "src\osd",
    "src\player",
    "src\remote",
    "src\scheduler",
    "src\tests",
    "src\util",
    "src\weather",

    "Config",

    "Docs",

    "Logs",

    "Media",
    "Media\Ambient",
    "Media\Commercials",
    "Media\Infomercials",
    "Media\Movies",
    "Media\Programming",
    "Media\Programming\Documentaries",
    "Media\Programming\Game_Shows",
    "Media\Programming\News",
    "Media\Programming\Sports",
    "Media\Programming\Talk_Shows",
    "Media\Programming\TV_Shows",
    "Media\Promos",
    "Media\Raw",
    "Media\Raw\Downloads",
    "Media\Raw\ToSort",
    "Media\Weather",

    "Metadata",

    "Schedules",
    "Schedules\Archives",
    "Schedules\Daily",
    "Schedules\Generated",
    "Schedules\Weekly",

    "Tools"
)

$RootFiles = @(
    ".gitignore",
    "CHANGELOG.md",
    "README.md",
    "ROADMAP.md",
    "requirements.txt"
)

$GitKeepFolders = @(
    "Cache",
    "ChannelConfigs",
    "Config",
    "Logs",
    "Metadata",

    "Schedules\Archives",
    "Schedules\Daily",
    "Schedules\Generated",
    "Schedules\Weekly",

    "Tools",

    "src\channel",
    "src\core",
    "src\engine",
    "src\guide",
    "src\metadata",
    "src\osd",
    "src\player",
    "src\remote",
    "src\scheduler",
    "src\tests",
    "src\util",
    "src\weather"
)

# ==========================================================
# Create Project Structure
# ==========================================================

Write-Section "Creating Project Folders"

foreach ($Folder in $Folders) {

    New-VistorFolder $Folder

}

# ==========================================================
# Create Root Files
# ==========================================================

Write-Section "Creating Project Files"

foreach ($File in $RootFiles) {

    New-VistorFile $File

}

# ==========================================================
# Create .gitkeep Files (file-protection)
# ==========================================================

Write-Section "Creating .gitkeep Files"

foreach ($Folder in $GitKeepFolders) {

    $FolderPath = Join-Path $ProjectRoot $Folder
    $GitKeep = Join-Path $FolderPath ".gitkeep"

    if (-not (Test-Path $GitKeep)) {

        New-Item `
            -ItemType File `
            -Path $GitKeep `
            -Force | Out-Null

        Write-Success "$Folder\.gitkeep"

    }
    else {

        Write-Skip "$Folder\.gitkeep"

    }

}

# ==========================================================
# Validation
# ==========================================================

Write-Section "Validating Project Structure"

$ValidationPassed = $true

foreach ($Folder in $Folders) {

    if (-not (Test-Path (Join-Path $ProjectRoot $Folder))) {

        Write-ErrorMessage "Missing Folder: $Folder"

        $ValidationPassed = $false

    }

}

foreach ($File in $RootFiles) {

    if (-not (Test-Path (Join-Path $ProjectRoot $File))) {

        Write-ErrorMessage "Missing File: $File"

        $ValidationPassed = $false

    }

}

if ($ValidationPassed) {

    Write-Success "Validation Passed"

}

# ==========================================================
# Summary
# ==========================================================

Write-Section "Project Summary"

Write-Host ""
Write-Host "Folders Created : $FoldersCreated"
Write-Host "Folders Skipped : $FoldersSkipped"
Write-Host ""
Write-Host "Files Created   : $FilesCreated"
Write-Host "Files Skipped   : $FilesSkipped"
Write-Host ""

if ($ValidationPassed) {

    Write-Host "Project Status  : READY FOR DEVELOPMENT" -ForegroundColor Green

}
else {

    Write-Host "Project Status  : VALIDATION FAILED" -ForegroundColor Red

}

Write-Host ""

Read-Host "Press Enter to exit"
