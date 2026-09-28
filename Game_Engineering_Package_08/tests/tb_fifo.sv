`timescale 1ns/1ps
module tb_fifo;
 parameter integer DEPTH=3;localparam integer CW=$clog2(DEPTH+1);
 reg clk=0,rst=1,in_valid=0,out_ready=0;reg[15:0] in_data=0;
 wire in_ready,out_valid;wire[15:0] out_data;wire[CW-1:0] count;
 sync_fifo #(.WIDTH(16),.DEPTH(DEPTH)) dut(.*);
 always #5 clk=~clk;
 reg[15:0] golden[0:DEPTH-1];integer n=0,k,j;reg push,pop,blocked=0;
 reg[31:0] rng=32'h00000733;
 function automatic [31:0] advance(input [31:0] v);advance=v*32'd1664525+32'd1013904223;endfunction
 initial begin
   for(k=0;k<6000;k=k+1) begin
     @(negedge clk);
     rng=advance(rng);rst=(k<2 || k%173==0);out_ready=rng[8];
     if(!blocked || rst) begin in_valid=rng[4];in_data=rng[31:16];end
     #1;
     if(rst)begin
       if(in_ready!==0 || out_valid!==0)$fatal(1,"reset must suppress transfers");
       push=0;pop=0;
     end else begin
       if(in_ready!==(n<DEPTH) || out_valid!==(n>0))$fatal(1,"handshake mismatch at %0d",k);
       if(n>0 && out_data!==golden[0])$fatal(1,"head mismatch at %0d",k);
       push=in_valid && in_ready;pop=out_ready && out_valid;
     end
     blocked=in_valid && !in_ready && !rst;
     @(posedge clk);
     if(rst)n=0;
     else begin
       if(pop)begin for(j=0;j<n-1;j=j+1)golden[j]=golden[j+1];n=n-1;end
       if(push)begin golden[n]=in_data;n=n+1;end
     end
     #1;if(count!==n)$fatal(1,"count mismatch at %0d",k);
   end
   $display("PASS tb_fifo DEPTH=%0d cycles=6000",DEPTH);$finish;
 end
endmodule
