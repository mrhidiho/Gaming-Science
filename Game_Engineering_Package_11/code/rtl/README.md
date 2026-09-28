# Optional RTL, formal and physical-flow exercises

These files are teaching inputs, not tested silicon or a finished verification dossier. Read `validation/VALIDATION_REPORT.md` for the actual execution status. You must run and review each tool route before recording its outcome. Pin tool revisions, solver, standard-cell libraries and the platform snapshot. Use only libraries you have permission to use. Never label the numerical Python timing exercise an STA result.

## Contract

Eight-bit values, four entries, one clock and synchronous active-high reset. Count and pointers reset; memory bits need not. `dout` is unspecified while empty and is sampled before the accepting pop edge. Full/empty use the pre-edge occupancy: a full simultaneous push/pop rejects the push; an empty simultaneous push/pop rejects the pop. Reset discards all queued values. This is not an asynchronous FIFO.

## Simulation

From `code/rtl`, with a recorded Icarus Verilog installation:

```sh
iverilog -g2012 -s tb_fifo -o fifo_sim teaching_fifo.sv tb_fifo.sv
vvp fifo_sim
```

The scoreboard checks accepted-item order, count, full/empty boundaries, wraparound and patterned reset. This finite test is not a universal ordering proof. Add randomized seeds and a systematic accepted-data property. Keep new outputs in your own evidence directory.

## Formal

With pinned Yosys, SBY, a compatible SMT solver and executable `boolector` available:

```sh
sby -f fifo.sby prove
sby -f fifo.sby cover
```

The supplied assertions concern occupancy, reset and accounting. They do **not** prove end-to-end data order or analog properties. The cover task must actually reach full and leave full; a proof with an impossible environment can be vacuous. Initial reset is assumed; later resets and requests remain unconstrained. A PASS applies to this RTL, assumptions and tool invocation only. A timeout/UNKNOWN is not PASS. Extend the property set with a reference queue or symbolic tracked data, add a deliberate mutation, and retain counterexamples before claiming the full Lesson 48.1 lab is complete.

## Physical design

Read official ORFS sources S09–S10 in the reference guide. In a clean, version-pinned ORFS checkout, copy this directory into `flow/designs/nangate45/teaching_fifo/`. From its `flow` directory, the documented pattern is:

```sh
make DESIGN_CONFIG=./designs/nangate45/teaching_fifo/config.mk
```

This is a flow-entry example, not a package installation command or a guarantee for every future revision. Verify the installed revision's config variables, paths and platform availability. Record synthesis, placement, clock-tree and routing status and extract actual paths from the generated logs. Review unconstrained endpoints and both min/max timing; inspect load and time units. The SDC deliberately times the synchronous reset and every other non-clock input. No timing exceptions are pre-approved. Add slew/drive assumptions appropriate to the actual library before comparing designs.

Retain command lines, config, input hashes, reports, warnings, tool versions and failed stages. Module 47 also requires the reasoned PPA comparison, checks and limitations in `templates/PHYSICAL_FLOW_REPORT.md`. Completion of routing or GDS output is not commercial fabrication signoff.
