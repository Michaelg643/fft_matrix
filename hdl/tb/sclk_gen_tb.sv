module sclk_gen_tb;
  logic clk;
  timeunit 1ns;
  timeprecision 100ps;
  realtime clk_per =

  sclk_gen DUT (
    .i_clk(clk),
    .i_rst(rst),
    .i_oe(oe),
    .i_clk_div(clk_div),

    .o_sclk(sclk),
    .o_sclk_f(sclk_f),
    .o_sclk_r(sclk_r)
  );

endmodule
