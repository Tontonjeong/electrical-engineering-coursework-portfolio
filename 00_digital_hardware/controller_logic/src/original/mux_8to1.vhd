----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 2024/11/07 22:13:53
-- Design Name: 
-- Module Name: mux_8to1 - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity mux_8to1 is 
    Port ( a : in STD_LOGIC;
           b : in STD_LOGIC;
           c : in STD_LOGIC;
           d : in STD_LOGIC;
           e : in STD_LOGIC;
           f : in STD_LOGIC;
           g : in STD_LOGIC;
           h : in STD_LOGIC;
           s2 : in STD_LOGIC;
           s1 : in STD_LOGIC;
           s0 : in STD_LOGIC;
           y : out STD_LOGIC);
end mux_8to1;

architecture Behavioral of mux_8to1 is
    component dec_3to8 is
        Port ( d2, d1, d0 : in STD_LOGIC;
               y0, y1, y2, y3, y4, y5, y6, y7 : out STD_LOGIC);
    end component;
    
    signal d0, d1, d2, d3, d4, d5, d6, d7 : std_logic;
    signal t0, t1, t2, t3, t4, t5, t6, t7 : std_logic;

begin
    U1: dec_3to8 port map (d2 => s2, d1 => s1, d0 => s0, 
                          y0 => d0, y1 => d1, y2 => d2, 
                          y3 => d3, y4 => d4, y5 => d5, 
                          y6 => d6, y7 => d7);
       
    t0 <= a and d0;
    t1 <= b and d1;
    t2 <= c and d2;
    t3 <= d and d3;
    t4 <= e and d4;
    t5 <= f and d5;       
    t6 <= g and d6;
    t7 <= h and d7;
    
    y <= t0 or t1 or t2 or t3 or t4 or t5 or t6 or t7;
end Behavioral;

