-- Author: michael
-- Company: idea machines
-- date 2022-09-25
--
-- name: lrck_gen.vhd
-- purpose: generates the lrck for i2s


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

entity lrck_gen is
generic (
    C_LRCK_SCLK_RATIO : integer := 32; -- Not necessarily equal to G_BIT_WIDTH
    C_MCLK_SCLK_RATIO : integer := 2
    );
port (
    --fpga interface
    i_clk:      in std_logic;
    i_rst:      in std_logic;
    i_oe:       in std_logic;

    o_sclk:     out std_logic;
    o_lrck:     out std_logic
    );
end lrck_gen;

architecture rtl of lrck_gen is
constant nbits : natural := integer(ceil(log2(real(C_LRCK_SCLK_RATIO))));
signal s_lrck_cnt: std_logic_vector(nbits-1 downto 0);

signal s_sclk:      std_logic;
signal s_sclk_f:    std_logic;
signal s_sclk_r:    std_logic;
signal s_sclk_d:    std_logic;
signal s_sclk_f_d:  std_logic;
signal s_sclk_r_d:  std_logic;
signal s_lrck:      std_logic;

--components
component sclk_gen is
generic (
    C_MCLK_SCLK_RATIO: integer := 4
    );
port (
    --fpga interface
    i_clk:      in std_logic;
    i_rst:      in std_logic;

    o_sclk:     out std_logic
    );
end component;

begin

  output_proc: process(all)
  begin
    if i_oe = '1' then
      o_sclk    <= s_sclk_d;
      o_lrck    <= s_lrck;
    else
      o_sclk    <= '0';
      o_lrck    <= '0';
    end if;
  end process;

  U_sclk_gen: sclk_gen
  generic map (
    C_MCLK_SCLK_RATIO => C_MCLK_SCLK_RATIO)
  port map (
  i_clk       => i_clk,
  i_rst       => i_rst,

  o_sclk      => s_sclk
  );

  -- Delay sclk for use in rising/falling edge gen
  sclk_delay: process(i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '1' then
        s_sclk_d <= '0';
      else
        s_sclk_d <= s_sclk;
      end if;
    end if;
  end process;
  s_sclk_r <= s_sclk and not s_sclk_d;
  s_sclk_f <= not s_sclk and s_sclk_d;

  lrck_gen_proc: process (i_clk)
  begin
    if rising_edge(i_clk) then
      if i_rst = '1' then
          s_lrck_cnt <= (others => '0');
          s_lrck <= '0';
      elsif i_oe <= '1' then
        if s_sclk_f = '1' then
          if s_lrck_cnt = std_logic_vector(to_unsigned(C_LRCK_SCLK_RATIO-1,s_lrck_cnt'length)) then
            s_lrck <= not s_lrck;
            s_lrck_cnt <= (others => '0');
          else
            s_lrck_cnt <= std_logic_vector(unsigned(s_lrck_cnt) + 1);
          end if;
        end if;
        s_sclk_d   <= s_sclk;
        s_sclk_f_d <= s_sclk_f;
        s_sclk_r_d <= s_sclk_r;
      end if;
    end if;
  end process;
end rtl;
