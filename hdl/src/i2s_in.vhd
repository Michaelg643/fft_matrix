-- Author: michael
-- Company: idea machines
-- date 2022-09-25
--
-- name: i2s_in.vhd
-- purpose: top level i2s interface

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use axisIfPkg.all;

--library unisim; -- https://forums.xilinx.com/t5/Welcome-Join/ODDR-use-in-vivado/m-p/735788/highlight/true#M41666
--use unisim.vcomponents.all;

entity i2s_in is
    generic (
        C_BIT_WIDTH : integer := 24;
        C_DIVIDE_BY : integer := 2
    );
    Port ( i_clk:   in std_logic; -- i_mclk
           i_rst:   in std_logic;

           --FPGA interface
           axisDownstreamAudioOut       : axisIfDownstream_t;

           --IC interface
           o_mclk:  out std_logic;
           o_sclk:  out std_logic;
           i_sd:    in  std_logic;
           o_lrck:  out std_logic);
end i2s_in;


architecture rtl of i2s_in is

------------------------------------------------------------------
--  SIGNALS
------------------------------------------------------------------
signal s_lrck_d:        std_logic;
signal s_lrck_dd:       std_logic;
signal s_wsp:           std_logic;
signal s_wsp_mclk_d:    std_logic;
signal s_wspp:          std_logic;
signal s_wsp_d:         std_logic;
signal s_wsp_dd:        std_logic;
signal s_wsp_d_reg:     std_logic_vector(2*G_DIVIDE_BY-1 downto 0);

signal s_cnt:       integer range 0 to G_BIT_WIDTH;
signal s_cnt_en:    std_logic;
signal s_cnt_en_d:  std_logic;
signal s_reg_en:    std_logic;
signal s_dec:       std_logic_vector(G_BIT_WIDTH downto 0);
signal s_data:      std_logic_vector(G_BIT_WIDTH-1 downto 0);

signal s_sclk:      std_logic;
signal s_lrsclk_fd: std_logic;
signal s_lrsclk_rd: std_logic;
signal s_sclk_f:    std_logic;
signal s_sclk_r:    std_logic;
signal s_sclk_f_d:  std_logic_vector(G_DIVIDE_BY - 1 downto 0);
signal s_sclk_r_d:  std_logic_vector(G_DIVIDE_BY - 1 downto 0);
signal s_lrck:      std_logic;


------------------------------------------------------------------
-- CONSTANTS
------------------------------------------------------------------

begin


  wsd_gen: process (i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '1' then
        s_lrck_d  <= '0';
        s_lrck_dd <= '0';
      elsif (s_lrsclk_rd = '1') then
        s_lrck_d  <= s_lrck;
        s_lrck_dd <= s_lrck_d;
      end if;
    end if;
  end process;
  s_wsp <= s_lrck_d xor s_lrck_dd;
  s_wspp <= s_lrck xor s_lrck_d;

  counter: process(i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '0' then
        s_cnt <= 0;
      elsif (s_sclk_f = '1') then
        if (s_wsp_d = '1') then
          s_cnt <= 0;
        elsif (s_dec(G_BIT_WIDTH) = '1') then
          null;
        else
          s_cnt <= s_cnt + 1;
        end if;
      end if;
    end if;
  end process;

  decoder: process(s_cnt)
  begin
    s_dec <= (others => '0');
    s_dec(s_cnt) <= '1';
  end process;

  s_cnt_en_d_gen: process (i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '0' then
        s_cnt_en_d  <= '0';
      elsif (s_sclk_r = '1') then
        s_cnt_en_d <= s_cnt_en;
      end if;
    end if;
  end process;
  s_reg_en <= s_cnt_en or s_cnt_en_d;

  register_input_data: process(i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '0' then
        s_data <= (others => '0');
        --if (s_sclk_r = '1' and s_lrsclk_rd = '0') then
      elsif (s_lrsclk_fd = '1') then
        if (s_wsp = '1') then
          s_data <= (others => '0');
        end if;
        if (s_dec(G_BIT_WIDTH) /= '1') then
          s_data(G_BIT_WIDTH - 1 - s_cnt) <= i_sd;
        end if;
      end if;
    end if;
  end process;

  output_data: process(i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '0' then
        o_audio <= (others => '0');
        o_ws <= '0';
        o_dr <= '0';
      elsif (s_sclk_r = '1') then
        o_ws <= not s_lrck_d; --because the output data will latch on the other channel than what is being received
        o_dr <= s_wsp;

        if (s_wspp = '1') then
          o_audio <= s_data; --only update when the WSP has happened
        end if;
      end if;
    end if;
  end process;

  pipeline_delay: process(i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '0' then
        s_sclk_f_d <= (others => '0');
        s_sclk_r_d <= (others => '0');
      else
        s_sclk   <= i_sclk;
        s_lrck   <= i_lrck;
        s_sclk_f_d <= s_sclk_f_d(G_DIVIDE_BY-2 downto 0) & i_sclk_f;
        s_sclk_r_d <= s_sclk_r_d(G_DIVIDE_BY-2 downto 0) & i_sclk_r;
        s_wsp_d_reg <= s_wsp_d_reg(2*G_DIVIDE_BY-2 downto 0) & s_wsp;
        s_wsp_dd <= s_wsp_d;
        s_wsp_mclk_d <= s_wsp;
      end if;
    end if;
  end process;
  s_lrsclk_fd <= s_sclk_f_d(G_DIVIDE_BY-1);
  s_lrsclk_rd <= s_sclk_r_d(G_DIVIDE_BY-1);
  s_sclk_f    <= s_sclk_f_d(0);
  s_sclk_r    <= s_sclk_r_d(0);
  s_wsp_d     <= s_wsp_d_reg(2*G_DIVIDE_BY-1);

  o_mclk <= i_clk;
  o_sclk <= s_sclk;
  o_lrck <= s_lrck_d;
end rtl;
