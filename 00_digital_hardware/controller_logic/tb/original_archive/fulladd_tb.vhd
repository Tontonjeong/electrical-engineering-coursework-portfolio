library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity fulladd_tb is
end fulladd_tb;

architecture Behavioral of fulladd_tb is
    component fulladd is
        Port ( a : in STD_LOGIC;
               b : in STD_LOGIC;
               cin : in STD_LOGIC;
               s : out STD_LOGIC;
               cout : out STD_LOGIC);
    end component;
    signal a, b, cin, s, cout : std_logic;
begin
    UUT: fulladd port map (a=>a, b=>b, cin=>cin, s=>s, cout=>cout);
    process
    begin
        a <= '0'; b <= '0'; cin <= '0'; wait for 20 ns;
        a <= '0'; b <= '0'; cin <= '1'; wait for 20 ns;
        a <= '0'; b <= '1'; cin <= '0'; wait for 20 ns;
        a <= '0'; b <= '1'; cin <= '1'; wait for 20 ns;
        a <= '1'; b <= '0'; cin <= '0'; wait for 20 ns;
        a <= '1'; b <= '0'; cin <= '1'; wait for 20 ns;
        a <= '1'; b <= '1'; cin <= '0'; wait for 20 ns;
        a <= '1'; b <= '1'; cin <= '1'; wait;
    end process;
end Behavioral;
