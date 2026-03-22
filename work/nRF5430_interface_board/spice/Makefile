# Makefile for nRF5430 Interface Board SPICE Simulations
# Usage: make all | make tb1 | make clean

NGSPICE = ngspice -b
TB_DIR = testbench
RES_DIR = results
LIB_DIR = lib

TESTBENCHES = tb_blink_read tb_code_clear tb_power_startup tb_load_dump \
              tb_analog_battery tb_analog_airflow tb_noise_rejection tb_static_glow

.PHONY: all clean $(TESTBENCHES)

all: $(RES_DIR) $(TESTBENCHES)
	@echo "All simulations complete."

$(RES_DIR):
	mkdir -p $(RES_DIR)

tb_blink_read: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_blink_read.cir > $(RES_DIR)/tb1_log.txt 2>&1
	@echo "TB1 (Blink Read) done."

tb_code_clear: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_code_clear.cir > $(RES_DIR)/tb2_log.txt 2>&1
	@echo "TB2 (Code Clear) done."

tb_power_startup: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_power_startup.cir > $(RES_DIR)/tb3_log.txt 2>&1
	@echo "TB3 (Power Startup) done."

tb_load_dump: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_load_dump.cir > $(RES_DIR)/tb4_log.txt 2>&1
	@echo "TB4 (Load Dump) done."

tb_analog_battery: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_analog_battery.cir > $(RES_DIR)/tb5_log.txt 2>&1
	@echo "TB5 (Analog Battery) done."

tb_analog_airflow: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_analog_airflow.cir > $(RES_DIR)/tb6_log.txt 2>&1
	@echo "TB6 (Analog Airflow) done."

tb_noise_rejection: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_noise_rejection.cir > $(RES_DIR)/tb7_log.txt 2>&1
	@echo "TB7 (Noise Rejection) done."

tb_static_glow: $(RES_DIR)
	$(NGSPICE) $(TB_DIR)/tb_static_glow.cir > $(RES_DIR)/tb8_log.txt 2>&1
	@echo "TB8 (Static Glow) done."

clean:
	rm -rf $(RES_DIR)/*.csv $(RES_DIR)/*.ps $(RES_DIR)/*.txt
