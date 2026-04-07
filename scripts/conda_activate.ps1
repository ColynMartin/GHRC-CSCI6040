# If execution policy blocks scripts: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#
# Dot-source this file so conda applies to your current PowerShell session:
#   cd "<path-to-GHRC-CSCI6040>"
#   . .\scripts\conda_activate.ps1
# Optional: choose env (default base)
#   . .\scripts\conda_activate.ps1 myenv

$hookPaths = @(
    "$env:USERPROFILE\anaconda3\shell\condabin\conda-hook.ps1",
    "$env:USERPROFILE\Anaconda3\shell\condabin\conda-hook.ps1",
    "$env:USERPROFILE\miniconda3\shell\condabin\conda-hook.ps1",
    "$env:USERPROFILE\Miniconda3\shell\condabin\conda-hook.ps1",
    "$env:ProgramData\Anaconda3\shell\condabin\conda-hook.ps1",
    "$env:ProgramData\Miniconda3\shell\condabin\conda-hook.ps1"
)

$hook = $hookPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $hook) {
    Write-Error @"
Could not find conda-hook.ps1. Install Anaconda/Miniconda, or from Anaconda Prompt run:

    conda init powershell

Then open a new terminal and try again.
"@
    return
}

. $hook
$envName = if ($args.Count -ge 1 -and $args[0]) { $args[0] } else { "base" }
conda activate $envName
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tip: list envs with: conda env list"
    return
}
Write-Host "Conda environment active: $envName"
Write-Host "Python: $(Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source)"
