#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CASE_ROOT="$REPO_ROOT/00_digital_hardware/controller_logic"
ARTIFACT_ROOT="${1:-$CASE_ROOT/build/artifacts/vhdl-verification}"
LOG_ROOT="$ARTIFACT_ROOT/logs"
VCD_ROOT="$ARTIFACT_ROOT/vcd"
WORK_ROOT="$CASE_ROOT/build/ghdl-ci"
SUMMARY="$ARTIFACT_ROOT/pass_fail_summary.csv"

mkdir -p "$LOG_ROOT" "$VCD_ROOT" "$ARTIFACT_ROOT/screenshots" "$WORK_ROOT"
printf '%s\n' \
  '"evidence_layer","testbench","result","checker","boundary"' \
  > "$SUMMARY"

run_logged() {
  local label="$1"
  shift
  printf '> ' > "$LOG_ROOT/$label.log"
  printf '%q ' "$@" >> "$LOG_ROOT/$label.log"
  printf '\n' >> "$LOG_ROOT/$label.log"
  "$@" 2>&1 | tee -a "$LOG_ROOT/$label.log"
}

run_original() {
  local testbench="$1"
  local stop_time="$2"
  local boundary="$3"
  shift 3
  local work="$WORK_ROOT/original-$testbench"
  mkdir -p "$work"
  run_logged "${testbench}_analyze" \
    ghdl -a --std=08 "--workdir=$work" "$@" \
    "$CASE_ROOT/tb/original_archive/${testbench}.vhd"
  run_logged "${testbench}_elaborate" \
    ghdl -e --std=08 "--workdir=$work" "$testbench"
  run_logged "${testbench}_simulate" \
    ghdl -r --std=08 "--workdir=$work" "$testbench" \
    "--stop-time=$stop_time" \
    "--vcd=$VCD_ROOT/original_${testbench}.vcd"
  printf '"ORIGINAL_STIMULUS_RERUN","%s","STIMULUS_COMPLETE","none","%s"\n' \
    "$testbench" "$boundary" >> "$SUMMARY"
}

run_original \
  fulladd_tb 160ns "original source + original stimulus" \
  "$CASE_ROOT/src/original/fulladd.vhd"
run_original \
  add_4bits_tb 200ns "original source + original stimulus" \
  "$CASE_ROOT/src/original/fulladd.vhd" \
  "$CASE_ROOT/src/original/add_4bits.vhd"
run_original \
  mealy_tb 260ns "original source + original stimulus" \
  "$CASE_ROOT/src/original/mealy_101.vhd"
run_original \
  mux_8to1_tb 400ns "original stimulus + recovered mux + reconstructed missing decoder dependency" \
  "$CASE_ROOT/src/portable_reconstruction/dec_3to8.vhd" \
  "$CASE_ROOT/src/original/mux_8to1.vhd"

SELF_WORK="$WORK_ROOT/self-checking"
mkdir -p "$SELF_WORK"
run_logged self_checking_analyze \
  ghdl -a --std=08 "--workdir=$SELF_WORK" \
  "$CASE_ROOT/src/original/fulladd.vhd" \
  "$CASE_ROOT/src/original/add_4bits.vhd" \
  "$CASE_ROOT/src/original/mux_8to1.vhd" \
  "$CASE_ROOT/src/original/mealy_101.vhd" \
  "$CASE_ROOT/src/portable_reconstruction/dec_3to8.vhd" \
  "$CASE_ROOT/src/portable_reconstruction/mux_8to1_4bits.vhd" \
  "$CASE_ROOT/src/portable_reconstruction/usr_4bit.vhd" \
  "$CASE_ROOT/tb/tb_fulladd.vhd" \
  "$CASE_ROOT/tb/tb_add_4bits.vhd" \
  "$CASE_ROOT/tb/tb_dec_3to8.vhd" \
  "$CASE_ROOT/tb/tb_mux_8to1.vhd" \
  "$CASE_ROOT/tb/tb_mux_8to1_4bits.vhd" \
  "$CASE_ROOT/tb/tb_mealy_101.vhd" \
  "$CASE_ROOT/tb/tb_usr_4bit.vhd"

for testbench in \
  tb_fulladd tb_add_4bits tb_dec_3to8 tb_mux_8to1 \
  tb_mux_8to1_4bits tb_mealy_101 tb_usr_4bit
do
  run_logged "${testbench}_elaborate" \
    ghdl -e --std=08 "--workdir=$SELF_WORK" "$testbench"
  run_logged "${testbench}_simulate" \
    ghdl -r --std=08 "--workdir=$SELF_WORK" "$testbench" \
    --assert-level=error \
    "--vcd=$VCD_ROOT/${testbench}.vcd"
  printf '"SELF_CHECKING_REGRESSION","%s","PASS","assertions","recovered originals where available; three explicit reconstructions"\n' \
    "$testbench" >> "$SUMMARY"
done

GHDL_VERSION="$(ghdl --version | head -n 1)"
python - "$ARTIFACT_ROOT/environment.json" "$GHDL_VERSION" <<'PY'
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

destination = Path(sys.argv[1])
payload = {
    "executed_utc": datetime.now(timezone.utc).isoformat(),
    "ghdl": sys.argv[2],
    "os": platform.platform(),
    "python": platform.python_version(),
    "github_sha": os.environ.get("GITHUB_SHA", "local"),
    "github_ref": os.environ.get("GITHUB_REF", "local"),
    "original_stimulus_result": "4 STIMULUS_COMPLETE; checker=none",
    "self_checking_result": "7 PASS; assertions enabled",
}
destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

cat > "$ARTIFACT_ROOT/screenshots/README.md" <<'EOF'
# Waveform rendering boundary

This CI run preserves simulator-generated VCD files. It does not label a
synthetic drawing as a simulator screenshot. Reviewed local GHDL waveform
exports remain in `docs/assets/results/digital/` with their source boundary.
EOF

printf 'CONTROLLER_LOGIC_REGRESSION_PASS original=4 self_check=7\n'
