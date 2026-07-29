library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity mealy_tb is
end mealy_tb;

architecture Behavioral of mealy_tb is
    component mealy
        port(
          clk : in std_logic;
          din : in std_logic;
          rst : in std_logic;
          dout : out std_logic
        );
    end component;
    signal clk : std_logic := '0';
    signal din : std_logic := '0';
    signal rst : std_logic := '0';
    signal dout : std_logic;
    constant clk_period : time := 20 ns;
begin
    UUT: mealy port map (clk => clk, din => din, rst => rst, dout => dout);
    clk_process: process
    begin
        clk <= '0'; wait for clk_period/2;
        clk <= '1'; wait for clk_period/2;
    end process;
    stim_proc: process
    begin
        rst <= '1'; wait for 100 ns;
        rst <= '0'; din <= '0'; wait for 20 ns;
        din <= '1'; wait for 20 ns;
        din <= '0'; wait for 20 ns;
        din <= '1'; wait for 20 ns;
        din <= '0'; wait for 20 ns;
        din <= '1'; wait for 20 ns;
        din <= '0'; wait for 20 ns;
        din <= '1';
        wait;
    end process;
end Behavioral;
