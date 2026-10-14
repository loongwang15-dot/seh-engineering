# Requires PowerShell 7. Preserve the recovery plan before replacing any installed file.
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$Target,
    [Parameter(Mandatory)][string]$Backup,
    [Parameter(Mandatory)][string]$Record
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Import-Module (Join-Path $PSScriptRoot 'seh-installation.psm1') -Force
$sehSourceRoot = Get-SehRoot $Source -MustExist
$sehTargetRoot = Get-SehRoot $Target -MustExist
$sehBackupRoot = Get-SehRoot $Backup
$sehRecordPath = [IO.Path]::GetFullPath($Record)
if (Test-Path -LiteralPath $sehBackupRoot) { throw 'Backup already exists; inspect the previous plan before retrying' }
if (Test-Path -LiteralPath $sehRecordPath) { throw 'Recovery record already exists; do not overwrite an earlier installation' }
foreach ($sehRoot in @($sehSourceRoot, $sehTargetRoot)) {
    $sehPrefix = $sehRoot + [IO.Path]::DirectorySeparatorChar
    if ($sehBackupRoot -eq $sehRoot -or $sehBackupRoot.StartsWith($sehPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        $sehRecordPath -eq $sehRoot -or $sehRecordPath.StartsWith($sehPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Backup and recovery record must be outside the source and installation directories'
    }
}
if ($sehSourceRoot -eq $sehTargetRoot) { throw 'Source and target must be different directories' }
if (-not (Test-Path -LiteralPath (Join-SehPath $sehSourceRoot 'SKILL.md') -PathType Leaf)) { throw 'Source SKILL.md not found' }
$sehIncoming = @(Get-SehFiles $sehSourceRoot | Sort-Object File)
# Validate all existing nested paths before creating backups or changing the target.
$null = @(Get-SehFiles $sehTargetRoot)
$sehEntries = @()
foreach ($sehFile in $sehIncoming) {
    $sehDestination = Join-SehPath $sehTargetRoot $sehFile.File
    $sehExisting = Test-Path -LiteralPath $sehDestination
    if ($sehExisting -and -not (Test-Path -LiteralPath $sehDestination -PathType Leaf)) { throw "Target collision: $($sehFile.File)" }
    $sehTemporaryName = '.seh-' + [guid]::NewGuid().ToString('N') + '.tmp'
    $sehTemporaryDirectory = [IO.Path]::GetDirectoryName($sehFile.File)
    $sehTemporaryRelative = if ($sehTemporaryDirectory) { Join-Path $sehTemporaryDirectory $sehTemporaryName } else { $sehTemporaryName }
    $sehEntries += [pscustomobject]@{
        File = $sehFile.File
        BeforeHash = $(if ($sehExisting) { Get-SehHash $sehDestination } else { $null })
        SourceHash = Get-SehHash $sehFile.Path
        TemporaryFile = $sehTemporaryRelative
        RestoreTemporaryFile = $(if ($sehTemporaryDirectory) { Join-Path $sehTemporaryDirectory ('.seh-restore-' + [guid]::NewGuid().ToString('N') + '.tmp') } else { '.seh-restore-' + [guid]::NewGuid().ToString('N') + '.tmp' })
        State = 'PLANNED'
    }
}
New-Item -ItemType Directory -Path $sehBackupRoot | Out-Null
foreach ($sehEntry in $sehEntries) {
    if ($null -eq $sehEntry.BeforeHash) { continue }
    $sehSaved = Join-SehPath $sehBackupRoot $sehEntry.File
    New-Item -ItemType Directory -Path (Split-Path -Parent $sehSaved) -Force | Out-Null
    Copy-Item -LiteralPath (Join-SehPath $sehTargetRoot $sehEntry.File) -Destination $sehSaved
    if ((Get-SehHash $sehSaved) -ne $sehEntry.BeforeHash) { throw "Backup mismatch: $($sehEntry.File)" }
}
$sehPlan = [pscustomobject]@{
    SchemaVersion = 1; Status = 'PREPARED'; Source = $sehSourceRoot; Target = $sehTargetRoot
    Backup = $sehBackupRoot; Entries = $sehEntries; Error = $null
    CopyIntegrity = 'UNVERIFIED'; Discovery = 'UNVERIFIED'; Runtime = 'UNVERIFIED'
}
Write-SehRecord $sehRecordPath $sehPlan
try {
    foreach ($sehEntry in $sehPlan.Entries) {
        $sehOriginal = Join-SehPath $sehSourceRoot $sehEntry.File
        $sehDestination = Join-SehPath $sehTargetRoot $sehEntry.File
        $sehTemporary = Join-SehPath $sehTargetRoot $sehEntry.TemporaryFile
        if ((Get-SehHash $sehOriginal) -ne $sehEntry.SourceHash) { throw "Source changed: $($sehEntry.File)" }
        $sehEntry.State = 'WRITING'
        $sehPlan.Status = 'INSTALLING'
        Write-SehRecord $sehRecordPath $sehPlan
        New-Item -ItemType Directory -Path (Split-Path -Parent $sehDestination) -Force | Out-Null
        Copy-Item -LiteralPath $sehOriginal -Destination $sehTemporary
        if ((Get-SehHash $sehTemporary) -ne $sehEntry.SourceHash) { throw "Staged copy mismatch: $($sehEntry.File)" }
        $sehExists = Test-Path -LiteralPath $sehDestination -PathType Leaf
        if (($null -eq $sehEntry.BeforeHash -and $sehExists) -or
            ($null -ne $sehEntry.BeforeHash -and (-not $sehExists -or (Get-SehHash $sehDestination) -ne $sehEntry.BeforeHash))) {
            throw "Preserve concurrent target change: $($sehEntry.File)"
        }
        # The verified temporary file is on the same volume; incomplete copying cannot truncate the destination.
        [IO.File]::Move($sehTemporary, $sehDestination, $true)
        $sehEntry.State = 'INSTALLED'
        Write-SehRecord $sehRecordPath $sehPlan
    }
    foreach ($sehEntry in $sehPlan.Entries) {
        if ((Get-SehHash (Join-SehPath $sehTargetRoot $sehEntry.File)) -ne $sehEntry.SourceHash) { throw "Installed mismatch: $($sehEntry.File)" }
    }
    $sehPlan.Status = 'INSTALLED'
    $sehPlan.CopyIntegrity = 'PASS'
    Write-SehRecord $sehRecordPath $sehPlan
    $sehPlan | Select-Object Status, Target, Backup, CopyIntegrity, Discovery, Runtime | ConvertTo-Json
} catch {
    $sehCause = $_.Exception.Message
    $sehPlan.Status = 'INTERRUPTED'
    $sehPlan.Error = $sehCause
    try { Write-SehRecord $sehRecordPath $sehPlan }
    catch { Write-Warning 'The earlier persistent recovery plan remains the recovery entry point.' }
    throw "Installation interrupted. Recovery plan: $sehRecordPath. Run rollback-seh.ps1 with this record, target and backup. Cause: $sehCause"
}
