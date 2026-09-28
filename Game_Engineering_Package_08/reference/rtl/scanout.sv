// Educational timing only. 80x60 total, 64x48 active; NOT an HDMI/VGA timing mode.
module scanout #(
 parameter integer H_ACTIVE=64,H_TOTAL=80,V_ACTIVE=48,V_TOTAL=60,
 parameter integer XW=(H_TOTAL<=1?1:$clog2(H_TOTAL)),
 parameter integer YW=(V_TOTAL<=1?1:$clog2(V_TOTAL))
)(input logic clk,rst,output logic [XW-1:0] x,output logic [YW-1:0] y,
  output logic active,frame_start,output logic [23:0] rgb);
  integer bar;
  always_comb begin
    active = !rst && (x<H_ACTIVE) && (y<V_ACTIVE);
    frame_start = !rst && (x==0) && (y==0);
    bar=(8*x)/H_ACTIVE;
    rgb=24'h000000;
    if (active) begin
      case(bar)
        0:rgb=24'hffffff; 1:rgb=24'hffff00; 2:rgb=24'h00ffff; 3:rgb=24'h00ff00;
        4:rgb=24'hff00ff; 5:rgb=24'hff0000; 6:rgb=24'h0000ff; default:rgb=24'h000000;
      endcase
      if(x>=20 && x<32 && y>=16 && y<28) rgb=24'hff8000;
    end
  end
  always_ff @(posedge clk) begin
    if (rst) begin x<='0; y<='0; end
    else if (x==H_TOTAL-1) begin
      x<='0;
      if(y==V_TOTAL-1) y<='0; else y<=y+1'b1;
    end else x<=x+1'b1;
  end
`ifndef SYNTHESIS
  initial if (H_ACTIVE<1 || V_ACTIVE<1 || H_TOTAL<H_ACTIVE || V_TOTAL<V_ACTIVE)
    $fatal(1,"invalid raster parameters");
`endif
endmodule
