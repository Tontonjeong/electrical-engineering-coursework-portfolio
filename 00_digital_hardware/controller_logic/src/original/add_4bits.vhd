----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 2024/10/24 22:30:44
-- Design Name: 
-- Module Name: add_4bits - Behavioral
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

entity add_4bits is
    Port ( a : in STD_LOGIC_VECTOR (3 downto 0);
           b : in STD_LOGIC_VECTOR (3 downto 0);
           cin : in STD_LOGIC;
           sum : out STD_LOGIC_VECTOR (3 downto 0);
           cout : out STD_LOGIC);
end add_4bits;

architecture Behavioral of add_4bits is
    component fulladd
        Port ( a, b, cin : in STD_LOGIC;
               s, cout : out STD_LOGIC);
        end component;
    
    signal tcout1, tcout2, tcout3 : std_logic;
    
begin
    U1: fulladd port map (a(0), b(0), cin, sum(0), tcout1);
    U2: fulladd port map (a(1), b(1), tcout1, sum(1), tcout2);
    U3: fulladd port map (a(2), b(2), tcout2, sum(2), tcout3);
    U4: fulladd port map (a(3), b(3), tcout3, sum(3), cout);

end Behavioral;

