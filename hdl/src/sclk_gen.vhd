-- Author: michael
-- Company: idea machines
-- date 2022-09-25
--
-- name: sclk_gen.vhd
-- purpose: generates the sclk for i2s


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

entity sclk_gen is
  generic (
    C_MCLK_SCLK_RATIO : integer := 192
  );
  port (
      i_clk     : in std_logic;
      i_rst     : in std_logic;

      o_sclk    : out std_logic
      );
end sclk_gen;

architecture rtl of sclk_gen is
signal s_sclk: std_logic;

constant nbits : natural := integer(ceil(log2(real(C_MCLK_SCLK_RATIO))));

signal s_sclk_cnt: std_logic_vector(nbits-1 downto 0);

begin

  o_sclk <= s_sclk;

  sclk_gen_proc: process(i_clk)
    begin
      if rising_edge(i_clk) then
        if i_rst = '1' then
          s_sclk <= '0';
          s_sclk_cnt <= (others => '0');
        elsif s_sclk_cnt = std_logic_vector(to_unsigned(C_MCLK_SCLK_RATIO, s_sclk_cnt'length)-1) then
          s_sclk_cnt <= (others => '0');
          s_sclk <= not s_sclk;
        else
          s_sclk_cnt <= std_logic_vector(unsigned(s_sclk_cnt) + 1);
        end if;
      end if;
  end process;
end rtl;
