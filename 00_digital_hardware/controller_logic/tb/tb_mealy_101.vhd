library ieee;
use ieee.std_logic_1164.all;
use std.env.all;

entity tb_mealy_101 is end;
architecture test of tb_mealy_101 is
  signal clk : std_logic := '0';
  signal rst : std_logic := '1';
  signal din, dout : std_logic := '0';
  type bit_array is array (natural range <>) of std_logic;
  constant stimulus : bit_array := ('1','0','1','0','1');
  constant expected : bit_array := ('0','0','1','0','1');
begin
  clk <= not clk after 5 ns;
  dut : entity work.mealy port map (clk, din, rst, dout);
  process
  begin
    wait until rising_edge(clk);
    rst <= '0';
    for i in stimulus'range loop
      wait until falling_edge(clk);
      din <= stimulus(i);
      wait for 1 ns;
      assert dout = expected(i) severity failure;
    end loop;
    report "PASS tb_mealy_101";
    stop;
    wait;
  end process;
end;
