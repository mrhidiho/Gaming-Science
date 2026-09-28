// Single-clock, synchronous active-high reset. Depth is fixed at four.
// Accepted operations use pre-edge full/empty. Not fall-through.
module teaching_fifo (
    input wire clk, input wire rst,
    input wire push, input wire pop,
    input wire [7:0] din,
    output wire [7:0] dout,
    output wire full, output wire empty,
    output reg [2:0] count
);
    reg [7:0] mem [0:3];
    reg [1:0] rd_ptr, wr_ptr;
    wire take_push = push && !full;
    wire take_pop = pop && !empty;
    assign full = count == 3'd4;
    assign empty = count == 3'd0;
    // dout is unspecified while empty; consumers must qualify it with !empty.
    assign dout = mem[rd_ptr];
    always @(posedge clk) begin
        if (rst) begin
            rd_ptr <= 0; wr_ptr <= 0; count <= 0;
        end else begin
            if (take_push) begin mem[wr_ptr] <= din; wr_ptr <= wr_ptr + 1'b1; end
            if (take_pop) rd_ptr <= rd_ptr + 1'b1;
            case ({take_push,take_pop})
              2'b10: count <= count + 1'b1;
              2'b01: count <= count - 1'b1;
              default: count <= count;
            endcase
        end
    end
`ifdef FORMAL
    reg past_valid = 0;
    always @(posedge clk) begin
        past_valid <= 1;
        // Reset required only at first sampled edge. Later reset remains free.
        if (!past_valid) assume(rst);
        if (past_valid) begin
            assert(count <= 4);
            if ($past(rst)) begin
                assert(count == 0);
                assert(rd_ptr == 0); assert(wr_ptr == 0);
            end else begin
                case ({$past(take_push),$past(take_pop)})
                  2'b10: assert(count == $past(count)+1'b1);
                  2'b01: assert(count == $past(count)-1'b1);
                  default: assert(count == $past(count));
                endcase
            end
            cover(full);
            cover($past(full) && !full);
        end
    end
`endif
endmodule
