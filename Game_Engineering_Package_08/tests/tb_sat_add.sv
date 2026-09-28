`timescale 1ns/1ps
module tb_sat_add;
 reg clk=0,rst=1,in_valid=0,out_ready=0;reg signed[15:0] a=0,b=0;
 wire in_ready,out_valid;wire signed[15:0] result;
 sat_add_stream dut(.*);always #5 clk=~clk;
 integer k,sum;reg valid=0,blocked=0;reg signed[15:0] expected;
 reg[31:0] rng=32'h00000735;
 initial begin
   for(k=0;k<5000;k=k+1)begin
     @(negedge clk);rng=rng*32'd1664525+32'd1013904223;
     rst=(k<2 || k%197==0);out_ready=rng[5];
     if(!blocked || rst)begin
       in_valid=rng[4];a=rng[31:16];b=rng[15:0];
       if(k%17==0)begin a=32767;b=1;end
       if(k%19==0)begin a=-32768;b=-1;end
     end
     #1;
     if(out_valid!==(!rst && valid) || in_ready!==(!rst && (!valid || out_ready)))$fatal(1,"handshake");
     if(out_valid && result!==expected)$fatal(1,"payload %0d expected %0d",result,expected);
     blocked=in_valid && !in_ready && !rst;
     if(rst)valid=0;
     else if(in_ready)begin
       valid=in_valid;
       if(in_valid)begin
         sum=$signed(a);sum=sum+$signed(b);
         if(sum>32767)expected=32767;else if(sum < -32768)expected=-32768;else expected=sum;
       end
     end
     @(posedge clk);#1;
   end
   $display("PASS tb_sat_add cycles=5000");$finish;
 end
endmodule
