# Copy this directory to <pinned-ORFS>/flow/designs/nangate45/teaching_fifo/.
# Nangate45 is an educational platform, not a fabrication commitment.
export DESIGN_NAME = teaching_fifo
export PLATFORM = nangate45
export VERILOG_FILES = $(DESIGN_HOME)/$(PLATFORM)/$(DESIGN_NAME)/teaching_fifo.sv
export SDC_FILE = $(DESIGN_HOME)/$(PLATFORM)/$(DESIGN_NAME)/teaching_fifo.sdc
export CORE_UTILIZATION = 30
export PLACE_DENSITY = 0.50
