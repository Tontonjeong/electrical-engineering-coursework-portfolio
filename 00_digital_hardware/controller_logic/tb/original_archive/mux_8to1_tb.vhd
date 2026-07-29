library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mux_8to1_tb is
end mux_8to1_tb;

architecture Behavioral of mux_8to1_tb is
    component mux_8to1
        port ( a, b, c, d, e, f, g, h : in STD_LOGIC;
               s2, s1, s0 : in STD_LOGIC;
               y : out STD_LOGIC);
    end component;
    signal a, b, c, d, e, f, g, h, s2, s1, s0, y : std_logic;
begin
    UUT: mux_8to1 port map(
        a=>a, b=>b, c=>c, d=>d, e=>e, f=>f, g=>g, h=>h,
        s2=>s2, s1=>s1, s0=>s0, y=>y
    );
    process
    begin
        a<='1'; b<='0'; c<='1'; d<='1'; e<='0'; f<='0'; g<='1'; h<='0';
        s2<='0'; s1<='0'; s0<='0'; wait for 50 ns;
        s2<='0'; s1<='0'; s0<='1'; wait for 50 ns;
        s2<='0'; s1<='1'; s0<='0'; wait for 50 ns;
        s2<='0'; s1<='1'; s0<='1'; wait for 50 ns;
        s2<='1'; s1<='0'; s0<='0'; wait for 50 ns;
        s2<='1'; s1<='0'; s0<='1'; wait for 50 ns;
        s2<='1'; s1<='1'; s0<='0'; wait for 50 ns;
        s2<='1'; s1<='1'; s0<='1'; wait;
    end process;
end Behavioral;
