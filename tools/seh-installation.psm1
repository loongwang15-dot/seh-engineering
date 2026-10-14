Set-StrictMode -Version Latest

function Get-SehRoot {
    param([Parameter(Mandatory)][string]$Path, [switch]$MustExist)
    $sehRoot = [IO.Path]::TrimEndingDirectorySeparator([IO.Path]::GetFullPath($Path))
    if ($MustExist -and -not (Test-Path -LiteralPath $sehRoot -PathType Container)) {
        throw "Directory not found: $sehRoot"
    }
    # Resolve the intentional user-skill root junction; nested links are rejected below.
    for ($sehDepth = 0; $sehDepth -lt 8 -and (Test-Path -LiteralPath $sehRoot); $sehDepth++) {
        $sehItem = Get-Item -LiteralPath $sehRoot -Force
        if (-not ($sehItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { return $sehRoot }
        $sehLinkTarget = @($sehItem.Target)[0]
        if (-not $sehLinkTarget) { throw "Unsupported root link: $sehRoot" }
        if (-not [IO.Path]::IsPathRooted($sehLinkTarget)) {
            $sehLinkTarget = Join-Path (Split-Path -Parent $sehRoot) $sehLinkTarget
        }
        $sehRoot = [IO.Path]::TrimEndingDirectorySeparator([IO.Path]::GetFullPath($sehLinkTarget))
    }
    if (Test-Path -LiteralPath $sehRoot) { throw 'Root link cycle or excessive link depth' }
    return $sehRoot
}

function Join-SehPath {
    param([Parameter(Mandatory)][string]$Root, [Parameter(Mandatory)][string]$Relative)
    if ([IO.Path]::IsPathRooted($Relative) -or @($Relative -split '[\\/]' | Where-Object { $_ -in '.', '..', '' }).Count) {
        throw "Invalid relative installation path: $Relative"
    }
    $sehPath = [IO.Path]::GetFullPath((Join-Path $Root $Relative))
    $sehPrefix = [IO.Path]::TrimEndingDirectorySeparator($Root) + [IO.Path]::DirectorySeparatorChar
    if (-not $sehPath.StartsWith($sehPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Installation path escapes root: $Relative"
    }
    $sehWalk = $sehPath
    while ($sehWalk -ne $Root) {
        if (Test-Path -LiteralPath $sehWalk) {
            if ((Get-Item -LiteralPath $sehWalk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "Nested link is not an installation file: $Relative"
            }
        }
        $sehWalk = Split-Path -Parent $sehWalk
        if (-not $sehWalk) { throw 'Unable to verify installation path' }
    }
    return $sehPath
}

function Get-SehFiles {
    param([Parameter(Mandatory)][string]$Root)
    $sehItems = @(Get-ChildItem -LiteralPath $Root -Recurse -Force)
    foreach ($sehItem in $sehItems) {
        $sehRelative = [IO.Path]::GetRelativePath($Root, $sehItem.FullName)
        if ($sehRelative -match '(^|[\\/])(__pycache__|\.git|\.pytest_cache)([\\/]|$)') { continue }
        if ($sehItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Unsupported nested link: $sehRelative" }
        if (-not $sehItem.PSIsContainer) {
            [pscustomobject]@{ File = $sehRelative; Path = (Join-SehPath $Root $sehRelative) }
        }
    }
}

function Get-SehHash {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Write-SehRecord {
    param([Parameter(Mandatory)][string]$Path, [Parameter(Mandatory)]$Record)
    $sehDirectory = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $sehDirectory -Force | Out-Null
    $sehTemporary = Join-Path $sehDirectory ('.seh-record-' + [guid]::NewGuid().ToString('N') + '.tmp')
    $sehBytes = [Text.UTF8Encoding]::new($false).GetBytes(($Record | ConvertTo-Json -Depth 12))
    $sehStream = [IO.File]::Open($sehTemporary, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $sehStream.Write($sehBytes, 0, $sehBytes.Length); $sehStream.Flush($true) }
    finally { $sehStream.Dispose() }
    [IO.File]::Move($sehTemporary, $Path, $true)
}

Export-ModuleMember -Function Get-SehRoot, Join-SehPath, Get-SehFiles, Get-SehHash, Write-SehRecord
