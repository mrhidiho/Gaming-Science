// One-entry elastic signed saturating adder. Unlike sync_fifo, can replace a
// departing output in the same edge. Inputs must remain stable while blocked.
module sat_add_stream #(parameter integer WIDTH=16)
(input logic clk,rst,input logic in_valid,
 input logic signed [WIDTH-1:0] a,b,output logic in_ready,
 output logic out_valid,output logic signed [WIDTH-1:0] result,input logic out_ready);
  localparam logic signed [WIDTH:0] MAXIMUM={2'b00,{(WIDTH-1){1'b1}}};
  localparam logic signed [WIDTH:0] MINIMUM={2'b11,{(WIDTH-1){1'b0}}};
  logic signed [WIDTH:0] sum;
  logic signed [WIDTH-1:0] clamped;
  logic valid_reg;
  always_comb begin
    sum = {a[WIDTH-1],a} + {b[WIDTH-1],b};
    if (sum > MAXIMUM) clamped = MAXIMUM[WIDTH-1:0];
    else if (sum < MINIMUM) clamped = MINIMUM[WIDTH-1:0];
    else clamped = sum[WIDTH-1:0];
    in_ready = !rst && (!valid_reg || out_ready);
    out_valid = !rst && valid_reg;
  end
  always_ff @(posedge clk) begin
    if (rst) begin valid_reg<=0; result<='0; end
    else if (in_ready) begin
      valid_reg <= in_valid;
      if (in_valid) result <= clamped;
    end
  end
`ifndef SYNTHESIS
  initial if (WIDTH<2) $fatal(1,"WIDTH must be at least 2");
`endif
endmodule
