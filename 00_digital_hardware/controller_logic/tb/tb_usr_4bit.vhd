library ieee;
use ieee.std_logic_1164.all;
use std.env.all;

entity tb_usr_4bit is end;
architecture test of tb_usr_4bit is
  signal clk : std_logic := '0';
  signal clear, d_in : std_logic := '0';
  signal s : std_logic_vector(1 downto 0) := "00";
  signal p_in, q : std_logic_vector(3 downto 0) := (others => '0');
begin
  clk <= not clk after 5 ns;
  dut : entity work.usr_4bit port map (clk, clear, s, d_in, p_in, q);
  process
  begin
    clear <= '1'; wait for 2 ns; assert q = "0000" severity failure;
    clear <= '0'; p_in <= "1010"; s <= "11";
    wait until rising_edge(clk); wait for 1 ns; assert q = "1010" severity failure;
    d_in <= '1'; s <= "01";
    wait until rising_edge(clk); wait for 1 ns; assert q = "1101" severity failure;
    d_in <= '0'; s <= "10";
    wait until rising_edge(clk); wait for 1 ns; assert q = "1010" severity failure;
    s <= "00";
    wait until rising_edge(clk); wait for 1 ns; assert q = "1010" severity failure;
    report "PASS tb_usr_4bit";
    stop;
    wait;
  end process;
end;
