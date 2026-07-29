library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity add_4bits_tb is
end add_4bits_tb;

architecture Behavioral of add_4bits_tb is
    component add_4bits is
        Port ( a : in STD_LOGIC_VECTOR (3 downto 0);
               b : in STD_LOGIC_VECTOR (3 downto 0);
               cin : in STD_LOGIC;
               sum : out STD_LOGIC_VECTOR (3 downto 0);
               cout : out STD_LOGIC);
    end component;
    signal a, b, sum : STD_LOGIC_VECTOR (3 downto 0);
    signal cin, cout : STD_LOGIC;
begin
    UUT: add_4bits port map (a=>a, b=>b, cin=>cin, sum=>sum, cout=>cout);
    process
    begin
        a <= "0001"; b <= "0011"; cin <= '0'; wait for 50 ns;
        a <= "0001"; b <= "0011"; cin <= '1'; wait for 50 ns;
        a <= "0101"; b <= "0011"; cin <= '1'; wait for 50 ns;
        a <= "0101"; b <= "1011"; cin <= '1'; wait;
    end process;
end Behavioral;
