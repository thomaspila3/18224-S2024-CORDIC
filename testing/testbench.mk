TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/tt_um_cordic.sv
TOPLEVEL = tt_um_cordic
MODULE = cordic_tb
SIM = verilator
EXTRA_ARGS += --trace -Wno-WIDTHTRUNC -Wno-UNOPTFLAT -Wno-fatal
include $(shell cocotb-config --makefiles)/Makefile.sim
