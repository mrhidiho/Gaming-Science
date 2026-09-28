// Conservative synchronous FIFO: no empty bypass, no full same-cycle replacement.
// RAM contents are not reset. out_data is meaningful only while out_valid==1.
module sync_fifo #(
  parameter integer WIDTH=16, DEPTH=3,
  parameter integer PTR_W=(DEPTH<=1 ? 1 : $clog2(DEPTH)),
  parameter integer COUNT_W=$clog2(DEPTH+1)
)(input logic clk,rst,
  input logic in_valid, input logic [WIDTH-1:0] in_data,
  output logic in_ready,
  output logic out_valid, output logic [WIDTH-1:0] out_data,
  input logic out_ready,
  output logic [COUNT_W-1:0] count);
  logic [WIDTH-1:0] memory [0:DEPTH-1];
  logic [PTR_W-1:0] read_ptr,write_ptr;
  logic push,pop;
  function automatic [PTR_W-1:0] advance(input [PTR_W-1:0] pointer);
    if (pointer == DEPTH-1) advance = '0;
    else advance = pointer + 1'b1;
  endfunction
  always_comb begin
    in_ready = !rst && (count < DEPTH);
    out_valid = !rst && (count != 0);
    out_data = memory[read_ptr];
    push = in_valid && in_ready;
    pop = out_valid && out_ready;
  end
  always_ff @(posedge clk) begin
    if (rst) begin read_ptr <= '0; write_ptr <= '0; count <= '0; end
    else begin
      if (push) begin memory[write_ptr] <= in_data; write_ptr <= advance(write_ptr); end
      if (pop) read_ptr <= advance(read_ptr);
      case ({push,pop})
        2'b10: count <= count + 1'b1;
        2'b01: count <= count - 1'b1;
        default: count <= count;
      endcase
    end
  end
`ifndef SYNTHESIS
  initial begin
    if (WIDTH<1 || DEPTH<1) $fatal(1,"WIDTH and DEPTH must be positive");
  end
`endif
endmodule
