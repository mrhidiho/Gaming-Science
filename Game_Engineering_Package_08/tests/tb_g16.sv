`timescale 1ns/1ps
module tb_g16;
 reg clk=0,rst=1;always #5 clk=~clk;
 wire [15:0] instr,data_rdata,pc,data_addr,data_wdata;wire data_we,stopped,fault;
 wire [1:0] fault_code;wire retire_valid;wire [31:0] retire_index;
 wire [15:0] retire_pc,retire_instr,retire_next_pc,retire_reg_value,retire_mem_addr,retire_mem_value;
 wire retire_reg_we,retire_mem_we,retire_halt;wire [2:0] retire_rd;
 reg[15:0] rom[0:255],ram[0:255];integer i,f,cycles;string program_file,trace_file,terminal_file;
 g16_core dut(.*);
 assign instr=(pc<256)?rom[pc]:16'h0000;
 assign data_rdata=(data_addr<256)?ram[data_addr]:16'h0000;
 always @(posedge clk)if(!rst && data_we)ram[data_addr]<=data_wdata;
 initial begin
   if(!$value$plusargs("PROG=%s",program_file))$fatal(1,"PROG is required");
   if(!$value$plusargs("TRACE=%s",trace_file))$fatal(1,"TRACE is required");
   if(!$value$plusargs("TERMINAL=%s",terminal_file))$fatal(1,"TERMINAL is required");
   for(i=0;i<256;i=i+1)begin rom[i]=0;ram[i]=0;end
   $readmemh(program_file,rom);f=$fopen(trace_file,"w");if(f==0)$fatal(1,"trace open");
   $fdisplay(f,"index,pc,instr,next_pc,reg_we,rd,reg_value,mem_we,mem_addr,mem_value,halt");
   @(posedge clk);#1;@(negedge clk);rst=0;
   for(cycles=0;cycles<10000;cycles=cycles+1)begin
     @(posedge clk);#1;
     if(retire_valid)$fdisplay(f,"%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d",
       retire_index,retire_pc,retire_instr,retire_next_pc,retire_reg_we,retire_rd,
       retire_reg_value,retire_mem_we,retire_mem_addr,retire_mem_value,retire_halt);
     if(stopped)begin
       $fclose(f);f=$fopen(terminal_file,"w");if(f==0)$fatal(1,"terminal open");
       $fdisplay(f,"%0d,%0d,%0d",fault,fault_code,pc);
       for(i=0;i<8;i=i+1)$fdisplay(f,"%0d",dut.regs[i]);
       for(i=0;i<256;i=i+1)$fdisplay(f,"%0d",ram[i]);
       $fclose(f);$display("PASS tb_g16 terminated cycles=%0d",cycles+1);$finish;
     end
   end
   $fatal(1,"execution limit");
 end
endmodule
