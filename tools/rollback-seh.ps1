# Requires PowerShell 7. Only restore this installation's files; preserve later edits.
param(
    [Parameter(Mandatory)][string]$Record,
    [Parameter(Mandatory)][string]$Target,
    [Parameter(Mandatory)][string]$Backup
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Import-Module (Join-Path $PSScriptRoot 'seh-installation.psm1') -Force
$sehRecordPath = [IO.Path]::GetFullPath($Record)
$sehTargetRoot = Get-SehRoot $Target -MustExist
$sehBackupRoot = Get-SehRoot $Backup -MustExist
$sehPlan = Get-Content -LiteralPath $sehRecordPath -Raw | ConvertFrom-Json
if ($sehPlan.SchemaVersion -isnot [long] -and $sehPlan.SchemaVersion -isnot [int]) { throw 'Invalid recovery schema type' }
if ($sehPlan.SchemaVersion -ne 1 -or $sehPlan.Target -ne $sehTargetRoot -or $sehPlan.Backup -ne $sehBackupRoot) {
    throw 'Recovery record does not match the explicitly supplied target and backup'
}
$sehSeen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
# Complete preflight before the first restore or removal, including interrupted writes.
foreach ($sehEntry in $sehPlan.Entries) {
    $sehDestination = Join-SehPath $sehTargetRoot $sehEntry.File
    if (-not $sehSeen.Add($sehDestination)) { throw 'Duplicate recovery path' }
    $sehCopyTemporary = Join-SehPath $sehTargetRoot $sehEntry.TemporaryFile
    $sehRestoreTemporary = Join-SehPath $sehTargetRoot $sehEntry.RestoreTemporaryFile
    if ([IO.Path]::GetFileName($sehCopyTemporary) -notmatch '^\.seh-[0-9a-f]{32}\.tmp$' -or
        [IO.Path]::GetFileName($sehRestoreTemporary) -notmatch '^\.seh-restore-[0-9a-f]{32}\.tmp$' -or
        (Split-Path -Parent $sehCopyTemporary) -ne (Split-Path -Parent $sehDestination) -or
        (Split-Path -Parent $sehRestoreTemporary) -ne (Split-Path -Parent $sehDestination)) {
        throw 'Invalid recovery temporary file'
    }
    if ($sehEntry.SourceHash -notmatch '^[0-9a-f]{64}$' -or
        ($null -ne $sehEntry.BeforeHash -and $sehEntry.BeforeHash -notmatch '^[0-9a-f]{64}$')) { throw 'Invalid recovery file hash' }
    if ($null -ne $sehEntry.BeforeHash) {
        $sehSaved = Join-SehPath $sehBackupRoot $sehEntry.File
        if (-not (Test-Path -LiteralPath $sehSaved -PathType Leaf) -or (Get-SehHash $sehSaved) -ne $sehEntry.BeforeHash) {
            throw "Backup changed: $($sehEntry.File)"
        }
    }
    if (Test-Path -LiteralPath $sehDestination) {
        if (-not (Test-Path -LiteralPath $sehDestination -PathType Leaf)) { throw "Target collision: $($sehEntry.File)" }
        $sehCurrentHash = Get-SehHash $sehDestination
        if ($sehCurrentHash -ne $sehEntry.SourceHash -and $sehCurrentHash -ne $sehEntry.BeforeHash) {
            throw "Preserve later change: $($sehEntry.File)"
        }
    } elseif ($null -ne $sehEntry.BeforeHash) { throw "Preserve later deletion: $($sehEntry.File)" }
}
$sehPlan.Status = 'ROLLING_BACK'
Write-SehRecord $sehRecordPath $sehPlan
foreach ($sehEntry in $sehPlan.Entries) {
    $sehDestination = Join-SehPath $sehTargetRoot $sehEntry.File
    if ($null -ne $sehEntry.BeforeHash) {
        if ((Get-SehHash $sehDestination) -ne $sehEntry.BeforeHash) {
            $sehRestoreTemporary = Join-SehPath $sehTargetRoot $sehEntry.RestoreTemporaryFile
            Copy-Item -LiteralPath (Join-SehPath $sehBackupRoot $sehEntry.File) -Destination $sehRestoreTemporary -Force
            if ((Get-SehHash $sehRestoreTemporary) -ne $sehEntry.BeforeHash) { throw "Staged restoration mismatch: $($sehEntry.File)" }
            $sehCurrentHash = Get-SehHash $sehDestination
            if ($sehCurrentHash -ne $sehEntry.SourceHash -and $sehCurrentHash -ne $sehEntry.BeforeHash) { throw "Preserve later change: $($sehEntry.File)" }
            [IO.File]::Move($sehRestoreTemporary, $sehDestination, $true)
            if ((Get-SehHash $sehDestination) -ne $sehEntry.BeforeHash) { throw "Restoration mismatch: $($sehEntry.File)" }
        }
    } elseif (Test-Path -LiteralPath $sehDestination -PathType Leaf) {
        # The preflight verified this exact absolute file is inside the explicit target and has this install's hash.
        Remove-Item -LiteralPath $sehDestination
    }
    $sehTemporary = Join-SehPath $sehTargetRoot $sehEntry.TemporaryFile
    if (Test-Path -LiteralPath $sehTemporary -PathType Leaf) {
        if ((Get-SehHash $sehTemporary) -eq $sehEntry.SourceHash) { Remove-Item -LiteralPath $sehTemporary }
        else { Write-Warning "Retained incomplete staged file: $($sehEntry.TemporaryFile)" }
    }
    $sehEntry.State = 'ROLLED_BACK'
    Write-SehRecord $sehRecordPath $sehPlan
}
$sehPlan.Status = 'ROLLED_BACK'
$sehPlan.CopyIntegrity = 'N/A'
Write-SehRecord $sehRecordPath $sehPlan
Write-Output 'Restored original files; unrelated files and later edits were preserved.'
