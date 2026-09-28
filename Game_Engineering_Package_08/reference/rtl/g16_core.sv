// G16 v1 educational single-cycle core, NOT RISC-V. External ROM/RAM reads
// are combinational in this reference. A synchronous block-RAM implementation
// requires a different controller. No ISA-compliance or target timing claim.
module g16_core(
 input logic clk,rst,input logic [15:0] instr,data_rdata,
 output logic [15:0] pc,data_addr,data_wdata,output logic data_we,
 output logic stopped,fault,output logic [1:0] fault_code,
 output logic retire_valid,output logic [31:0] retire_index,
 output logic [15:0] retire_pc,retire_instr,retire_next_pc,
 output logic retire_reg_we,output logic [2:0] retire_rd,
 output logic [15:0] retire_reg_value,output logic retire_mem_we,
 output logic [15:0] retire_mem_addr,retire_mem_value,output logic retire_halt);
 logic [15:0] regs [0:7];
 logic [31:0] retired_count;
 logic [3:0] opcode;logic [2:0] rd,ra,rb;
 logic [15:0] next_pc,value,address;logic write_reg,write_mem,do_halt;
 logic [1:0] decode_fault;
 integer i;
 always_comb begin
   opcode=instr[15:12];rd=instr[11:9];ra=instr[8:6];rb=instr[5:3];
   next_pc=pc+16'd1;value=0;address=0;write_reg=0;write_mem=0;do_halt=0;decode_fault=0;
   if (pc>=256) decode_fault=1; // fetch fault
   else case(opcode)
     4'h0: if(instr!=16'h0000) decode_fault=2;
     4'h1: begin write_reg=1;value={{7{instr[8]}},instr[8:0]};end
     4'h2,4'h3: begin
       if(instr[2:0]!=0) decode_fault=2;
       else begin write_reg=1;
         if(opcode==4'h2) value=regs[ra]+regs[rb]; else value=regs[ra]-regs[rb];
       end
     end
     4'h4,4'h5: begin
       address=regs[ra]+{{10{instr[5]}},instr[5:0]};
       if(address>=256) decode_fault=3;
       else if(opcode==4'h4) begin write_reg=1;value=data_rdata;end
       else write_mem=1;
     end
     4'h6: if(regs[rd]==0) next_pc=pc+16'd1+{{7{instr[8]}},instr[8:0]};
     4'h7: begin
       if(instr[11:8]!=0) decode_fault=2;
       else next_pc={8'd0,instr[7:0]};
     end
     4'hf: begin if(instr!=16'hf000) decode_fault=2;else do_halt=1;end
     default:decode_fault=2;
   endcase
   data_addr=address;data_wdata=regs[rd];
   data_we=write_mem && !stopped && !rst && decode_fault==0;
 end
 always_ff @(posedge clk) begin
   if(rst) begin
     pc<=0;stopped<=0;fault<=0;fault_code<=0;retired_count<=0;retire_valid<=0;
     retire_index<=0;retire_pc<=0;retire_instr<=0;retire_next_pc<=0;
     retire_reg_we<=0;retire_rd<=0;retire_reg_value<=0;
     retire_mem_we<=0;retire_mem_addr<=0;retire_mem_value<=0;retire_halt<=0;
     for(i=0;i<8;i=i+1) regs[i]<=0;
   end else begin
     retire_valid<=0;
     if(!stopped) begin
       if(decode_fault!=0) begin stopped<=1;fault<=1;fault_code<=decode_fault;end
       else begin
         if(write_reg && rd!=0) regs[rd]<=value;
         regs[0]<=0;pc<=next_pc;stopped<=do_halt;
         retire_valid<=1;retire_index<=retired_count;retired_count<=retired_count+1;
         retire_pc<=pc;retire_instr<=instr;retire_next_pc<=next_pc;
         retire_reg_we<=write_reg && rd!=0;
         retire_rd<=(write_reg && rd!=0)?rd:3'd0;
         retire_reg_value<=(write_reg && rd!=0)?value:16'd0;
         retire_mem_we<=write_mem;
         retire_mem_addr<=write_mem?address:16'd0;
         retire_mem_value<=write_mem?regs[rd]:16'd0;
         retire_halt<=do_halt;
       end
     end
   end
 end
endmodule
