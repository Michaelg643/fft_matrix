-- Author: michael
-- Company: idea machines
-- date 2022-07-13
--
-- name: fft_matrix_top.vhd
-- purpose: This is the top level module of the FFT RGB LED matrix project 

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library unisim;
use unisim.vcomponents.all;

entity fft_matrix is
  port(
        i_clk           :  in std_logic; -- FPGA clock domain
        i_rst           :  in std_logic; -- active high;
        i_en            :  in std_logic; -- enable, active high, synchronous to i_clk

        -- Audio Interface
        o_mclk          : out std_logic;
        o_sclk          : out std_logic;
        i_sd            :  in std_logic;
        o_lrck          : out std_logic;
        
        -- data egression, synchronous to o_pclk
        o_pclk          : out std_logic;
        o_r0            : out std_logic;
        o_g0            : out std_logic;
        o_b0            : out std_logic;
        o_r1            : out std_logic;
        o_g1            : out std_logic;
        o_b1            : out std_logic;
        o_addr_a        : out std_logic;
        o_addr_b        : out std_logic;
        o_addr_c        : out std_logic;
        o_addr_d        : out std_logic;
        o_matrix_latch  : out std_logic;
        o_matrix_en     : out std_logic
        );
end fft_matrix;

architecture rtl of fft_matrix is

begin


end architecture rtl;
