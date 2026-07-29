$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$caseRoot = Join-Path $repoRoot "00_digital_hardware\controller_logic"
$resultRoot = Join-Path $caseRoot "results"
$vcdRoot = Join-Path $resultRoot "vcd"
$buildRoot = Join-Path $caseRoot "build\ghdl-local"
New-Item -ItemType Directory -Path $resultRoot, $vcdRoot, $buildRoot -Force | Out-Null

$ghdlCommand = Get-Command ghdl -ErrorAction SilentlyContinue
if ($ghdlCommand) {
    $ghdl = $ghdlCommand.Source
} else {
    $wingetRoot = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages"
    $ghdl = Get-ChildItem -LiteralPath $wingetRoot -Recurse -Filter ghdl.exe |
        Select-Object -First 1 -ExpandProperty FullName
}
if (-not $ghdl -or -not (Test-Path -LiteralPath $ghdl)) {
    throw "GHDL executable not found."
}

$log = Join-Path $resultRoot "ghdl_6_0_0_local_regression.log"
$summary = Join-Path $resultRoot "ghdl_6_0_0_local_summary.csv"
$version = (& $ghdl --version | Select-Object -First 1)
$rows = [System.Collections.Generic.List[object]]::new()

function Invoke-Ghdl {
    param([string[]]$Arguments)
    $commandLine = "ghdl " + ($Arguments -join " ")
    Add-Content -LiteralPath $log -Value "`n> $commandLine" -Encoding utf8
    $output = @(& $ghdl @Arguments 2>&1 | ForEach-Object { [string]$_ })
    foreach ($line in $output) {
        Add-Content -LiteralPath $log -Value $line -Encoding utf8
        Write-Output $line
    }
    if ($LASTEXITCODE -ne 0) {
        throw "GHDL failed: $($Arguments -join ' ')"
    }
}

Set-Content -LiteralPath $log -Value "tool=$version`nexecuted_kst=$(Get-Date -Format o)" -Encoding utf8

$designs = @(
    "src\original\fulladd.vhd",
    "src\original\add_4bits.vhd",
    "src\original\mux_8to1.vhd",
    "src\original\mealy_101.vhd",
    "src\portable_reconstruction\dec_3to8.vhd",
    "src\portable_reconstruction\mux_8to1_4bits.vhd",
    "src\portable_reconstruction\usr_4bit.vhd"
)

# Source-derived original stimuli are deliberately executed first.  These TBs
# contain no assertions, so completion is recorded as STIMULUS_COMPLETE, not PASS.
$originalTests = @(
    @{ Name = "fulladd_tb"; File = "tb\original_archive\fulladd_tb.vhd"; Stop = "160ns"; Boundary = "original source + original stimulus" },
    @{ Name = "add_4bits_tb"; File = "tb\original_archive\add_4bits_tb.vhd"; Stop = "200ns"; Boundary = "original source + original stimulus" },
    @{ Name = "mealy_tb"; File = "tb\original_archive\mealy_tb.vhd"; Stop = "260ns"; Boundary = "original source + original stimulus" },
    @{ Name = "mux_8to1_tb"; File = "tb\original_archive\mux_8to1_tb.vhd"; Stop = "400ns"; Boundary = "original stimulus + recovered mux + reconstructed missing decoder dependency" }
)

foreach ($test in $originalTests) {
    $work = Join-Path $buildRoot ("original-" + $test.Name)
    New-Item -ItemType Directory -Path $work -Force | Out-Null
    $sourceSet = @()
    if ($test.Name -eq "fulladd_tb") { $sourceSet = @("src\original\fulladd.vhd") }
    if ($test.Name -eq "add_4bits_tb") { $sourceSet = @("src\original\fulladd.vhd", "src\original\add_4bits.vhd") }
    if ($test.Name -eq "mealy_tb") { $sourceSet = @("src\original\mealy_101.vhd") }
    if ($test.Name -eq "mux_8to1_tb") { $sourceSet = @("src\portable_reconstruction\dec_3to8.vhd", "src\original\mux_8to1.vhd") }
    $files = @($sourceSet + $test.File | ForEach-Object { Join-Path $caseRoot $_ })
    Invoke-Ghdl -Arguments (@("-a", "--std=08", "--workdir=$work") + $files)
    Invoke-Ghdl -Arguments @("-e", "--std=08", "--workdir=$work", $test.Name)
    Invoke-Ghdl -Arguments @(
        "-r", "--std=08", "--workdir=$work", $test.Name,
        "--stop-time=$($test.Stop)",
        "--vcd=$(Join-Path $vcdRoot ("original_" + $test.Name + ".vcd"))"
    )
    Add-Content -LiteralPath $log -Value "RESULT $($test.Name)=STIMULUS_COMPLETE checker=none" -Encoding utf8
    $rows.Add([pscustomobject]@{
        evidence_layer = "ORIGINAL_STIMULUS_RERUN"
        testbench = $test.Name
        result = "STIMULUS_COMPLETE"
        checker = "none"
        boundary = $test.Boundary
    })
}

$selfChecks = @(
    "tb_fulladd", "tb_add_4bits", "tb_dec_3to8", "tb_mux_8to1",
    "tb_mux_8to1_4bits", "tb_mealy_101", "tb_usr_4bit"
)
$portableWork = Join-Path $buildRoot "self-checking"
New-Item -ItemType Directory -Path $portableWork -Force | Out-Null
$files = @(
    $designs + ($selfChecks | ForEach-Object { "tb\$_.vhd" }) |
    ForEach-Object { Join-Path $caseRoot $_ }
)
Invoke-Ghdl -Arguments (@("-a", "--std=08", "--workdir=$portableWork") + $files)
foreach ($test in $selfChecks) {
    Invoke-Ghdl -Arguments @("-e", "--std=08", "--workdir=$portableWork", $test)
    Invoke-Ghdl -Arguments @(
        "-r", "--std=08", "--workdir=$portableWork", $test,
        "--assert-level=error",
        "--vcd=$(Join-Path $vcdRoot ("$test.vcd"))"
    )
    Add-Content -LiteralPath $log -Value "RESULT $test=PASS checker=assertions" -Encoding utf8
    $rows.Add([pscustomobject]@{
        evidence_layer = "SELF_CHECKING_REGRESSION"
        testbench = $test
        result = "PASS"
        checker = "assertions"
        boundary = "Recovered originals where available; three explicitly reconstructed dependencies/designs"
    })
}

$rows | Export-Csv -LiteralPath $summary -NoTypeInformation -Encoding utf8
Write-Output "CONTROLLER_LOGIC_REGRESSION_PASS original=4 self_check=7"
