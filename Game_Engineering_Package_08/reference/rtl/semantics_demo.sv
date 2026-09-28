// Reference example. Both registers read OLD values on the active edge.
module semantics_demo(input logic clk,rst,input logic [7:0] d,
                      output logic [7:0] q1,q2);
  always_ff @(posedge clk) begin
    if (rst) begin q1 <= 0; q2 <= 0; end
    else begin q1 <= d; q2 <= q1; end
  end
endmodule
