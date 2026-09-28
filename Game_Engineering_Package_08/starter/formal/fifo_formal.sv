// STARTER properties, not a delivered proof. Add ordering and reachability checks.
// Clock is constrained by the SBY formal flow, not a generated fabric clock.
module fifo_formal(input wire clk);
 localparam DEPTH=3,WIDTH=8,CW=$clog2(DEPTH+1);
 (* anyseq *) reg rst,in_valid,out_ready;
 (* anyseq *) reg[WIDTH-1:0] in_data;
 wire in_ready,out_valid;wire[WIDTH-1:0] out_data;wire[CW-1:0] count;
 sync_fifo #(.WIDTH(WIDTH),.DEPTH(DEPTH)) dut(.*);
 reg past_valid=0;
 always @(posedge clk) begin
   past_valid<=1;
   if(!past_valid)assume(rst);
   if(past_valid)begin
     assert(count<=DEPTH);
     if($past(rst))assert(count==0);
     if(!$past(rst) && !rst && $past(out_valid && !out_ready))begin
       assert(out_valid);assert(out_data==$past(out_data));
     end
     // Input sender contract; never assume properties of DUT outputs.
     if(!$past(rst) && !rst && $past(in_valid && !in_ready))begin
       assume(in_valid);assume(in_data==$past(in_data));
     end
     cover(!rst && count==DEPTH);
     cover(!rst && in_valid && in_ready && out_valid && out_ready);
   end
 end
endmodule
