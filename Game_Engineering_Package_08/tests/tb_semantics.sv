`timescale 1ns/1ps
module tb_semantics;
 reg clk=0,rst=1;reg[7:0] d=0;wire[7:0] q1,q2;
 always #5 clk=~clk;
 semantics_demo dut(.*);
 initial begin
  @(posedge clk);#1;if(q1!==0 || q2!==0)$fatal(1,"reset");
  @(negedge clk);rst=0;d=7;
  @(posedge clk);#1;if(q1!==7 || q2!==0)$fatal(1,"old q1 required");
  @(negedge clk);d=9;
  @(posedge clk);#1;if(q1!==9 || q2!==7)$fatal(1,"pipeline order");
  @(negedge clk);rst=1;d=33;
  @(posedge clk);#1;if(q1!==0 || q2!==0)$fatal(1,"reset priority");
  $display("PASS tb_semantics");$finish;
 end
endmodule
