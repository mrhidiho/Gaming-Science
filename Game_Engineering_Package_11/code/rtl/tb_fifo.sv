`timescale 1ns/1ps
module tb_fifo;
    reg clk=0, rst=1, push=0, pop=0;
    reg [7:0] din=0;
    wire [7:0] dout;
    wire full,empty;
    wire [2:0] count;
    teaching_fifo dut(clk,rst,push,pop,din,dout,full,empty,count);
    always #5 clk=~clk;
    reg [7:0] expected[0:3];
    integer used=0, i, tick;
    reg ap, aq;
    task drive(input reg p, input reg q, input reg reset_now, input reg [7:0] value);
        begin
            @(negedge clk); push=p; pop=q; rst=reset_now; din=value;
            @(posedge clk);
            ap = p && used<4;
            aq = q && used>0;
            if(reset_now) used=0;
            else begin
                if(aq) begin
                    if(dout !== expected[0]) $fatal(1,"FIFO data order mismatch");
                    for(i=0;i<3;i=i+1) expected[i]=expected[i+1];
                    used=used-1;
                end
                if(ap) begin expected[used]=value; used=used+1; end
            end
            #1;
            if(count !== used[2:0]) $fatal(1,"FIFO occupancy mismatch");
            if(full !== (used==4) || empty !== (used==0)) $fatal(1,"FIFO flags mismatch");
        end
    endtask
    initial begin
        drive(0,0,1,0);
        for(tick=0;tick<4;tick=tick+1) drive(1,0,0,tick);
        drive(1,1,0,99); // Full: reject push, accept pop.
        for(tick=0;tick<4;tick=tick+1) drive(0,1,0,0);
        drive(1,1,0,77); // Empty: accept push, reject pop.
        for(tick=0;tick<300;tick=tick+1)
            drive(tick%3!=0,tick%4!=0,tick%97==0,tick);
        drive(0,0,1,0);
        $display("PASS: FIFO directed + 300 patterned cycles"); $finish;
    end
endmodule
