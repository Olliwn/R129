#!/bin/bash
# run_all.sh - Execute all SPICE testbenches and collect results
# Usage: cd spice/ && ./run_all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TB_DIR="$SCRIPT_DIR/testbench"
RESULTS_DIR="$SCRIPT_DIR/results"
REPORT="$RESULTS_DIR/simulation_report.txt"

mkdir -p "$RESULTS_DIR"

echo "============================================" | tee "$REPORT"
echo "nRF5430 Interface Board - Simulation Report" | tee -a "$REPORT"
echo "Date: $(date)" | tee -a "$REPORT"
echo "Simulator: $(ngspice --version 2>&1 | head -1)" | tee -a "$REPORT"
echo "============================================" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

PASS=0
FAIL=0
TOTAL=0

run_testbench() {
    local tb_file="$1"
    local tb_name="$(basename "$tb_file" .cir)"
    TOTAL=$((TOTAL + 1))

    echo "--- Running: $tb_name ---" | tee -a "$REPORT"

    if ngspice -b "$tb_file" > "$RESULTS_DIR/${tb_name}_log.txt" 2>&1; then
        echo "  STATUS: COMPLETED" | tee -a "$REPORT"
        PASS=$((PASS + 1))

        # Extract .meas results if present
        if grep -q "^[a-z_]" "$RESULTS_DIR/${tb_name}_log.txt" 2>/dev/null; then
            grep -E "^(v_|t_|i_)" "$RESULTS_DIR/${tb_name}_log.txt" >> "$REPORT" 2>/dev/null || true
        fi
    else
        echo "  STATUS: FAILED (ngspice returned error)" | tee -a "$REPORT"
        FAIL=$((FAIL + 1))
        # Show last 10 lines of log for debugging
        echo "  Last 10 lines of output:" | tee -a "$REPORT"
        tail -10 "$RESULTS_DIR/${tb_name}_log.txt" | tee -a "$REPORT"
    fi
    echo "" | tee -a "$REPORT"
}

echo "Phase A: Component/Path-Level Tests" | tee -a "$REPORT"
echo "------------------------------------" | tee -a "$REPORT"

run_testbench "$TB_DIR/tb_blink_read.cir"
run_testbench "$TB_DIR/tb_code_clear.cir"
run_testbench "$TB_DIR/tb_analog_battery.cir"
run_testbench "$TB_DIR/tb_analog_airflow.cir"

echo "Phase B: Power Supply Tests" | tee -a "$REPORT"
echo "----------------------------" | tee -a "$REPORT"

run_testbench "$TB_DIR/tb_power_startup.cir"
run_testbench "$TB_DIR/tb_load_dump.cir"

echo "Phase C: System-Level Tests" | tee -a "$REPORT"
echo "----------------------------" | tee -a "$REPORT"

run_testbench "$TB_DIR/tb_noise_rejection.cir"
run_testbench "$TB_DIR/tb_static_glow.cir"

echo "============================================" | tee -a "$REPORT"
echo "SUMMARY: $PASS/$TOTAL completed, $FAIL failed" | tee -a "$REPORT"
echo "============================================" | tee -a "$REPORT"
