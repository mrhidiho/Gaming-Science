`timescale 1ns/1ps
module tb_scanout;
 reg clk=0,rst=1;wire[6:0] x;wire[5:0] y;wire active,frame_start;wire[23:0] rgb;
 scanout dut(.*);always #5 clk=~clk;
 integer k,ex,ey,active_count=0,frames=0,f;
 reg[23:0] expected;string capture;
 initial begin
   if(!$value$plusargs("CAPTURE=%s",capture))capture="scanout.csv";
   f=$fopen(capture,"w");if(f==0)$fatal(1,"cannot open capture");
   $fdisplay(f,"x,y,rgb");
   @(posedge clk);#1;@(negedge clk);rst=0;
   for(k=0;k<9600;k=k+1)begin
     #1;ex=k%80;ey=(k/80)%60;
     if(x!==ex || y!==ey)$fatal(1,"coordinate");
     if(active!==((ex<64)&&(ey<48)))$fatal(1,"active");
     if(frame_start!==((ex==0)&&(ey==0)))$fatal(1,"frame_start");
     if(active)begin active_count=active_count+1;if(k<4800)$fdisplay(f,"%0d,%0d,%0d",x,y,rgb);end
     if(frame_start)frames=frames+1;
     @(posedge clk);#1;@(negedge clk);
   end
   if(active_count!=6144 || frames!=2)$fatal(1,"frame totals");
   $fclose(f);$display("PASS tb_scanout frames=2");$finish;
 end
endmodule
