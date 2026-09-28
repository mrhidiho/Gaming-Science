# Teaching constraints in ns. Verify library and tool time units before use.
# Reset is SYNCHRONOUS and timed with all other non-clock inputs.
create_clock -name core_clk -period 10.0 [get_ports clk]
set_clock_uncertainty -setup 0.10 [get_clocks core_clk]
set_clock_uncertainty -hold 0.05 [get_clocks core_clk]
set nonclock_inputs [get_ports {rst push pop din*}]
set_input_delay -clock core_clk -max 1.00 $nonclock_inputs
set_input_delay -clock core_clk -min 0.20 $nonclock_inputs
set_output_delay -clock core_clk -max 1.00 [all_outputs]
set_output_delay -clock core_clk -min 0.20 [all_outputs]
# Educational load. Verify the library capacitance unit; do not assume pF.
set_load 0.01 [all_outputs]
# No false paths or multicycle exceptions are justified for this block.
