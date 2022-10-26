`timescale 1ns/1ps

module lrck_gen_tb;
  logic clk = 1'b0;
  logic rst = 1'b1;
  logic oe  = 1'b0;

  logic sclk;
  logic lrck;

  parameter CLK_PER_DIV2 = 2; // 250 MHz

  // Drive Clocks
  always #CLK_PER_DIV2 clk <= ~clk;

  task sync_wait(input integer cycles);
    begin
      for (int i=0;i<cycles;i=i+1)
        @(posedge clk);
    end
  endtask

  task sync_reset(input integer cycles);
    begin
      rst = 1'b1;
      sync_wait(cycles);
      rst = 1'b0;
    end
  endtask

  initial begin
    rst <= 1'b1;
    sync_wait(4096);
    rst <= 1'b0;
    oe <= 1'b1;
  end

  lrck_gen #
    ( .C_LRCK_SCLK_RATIO(32),
      .C_MCLK_SCLK_RATIO(2)
    ) DUT (
    .i_clk(clk),
    .i_rst(rst),
    .i_oe(oe),

    .o_sclk(sclk),
    .o_lrck(lrck)
  );

endmodule
