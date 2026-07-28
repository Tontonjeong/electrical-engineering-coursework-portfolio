library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity tb_mux_8to1 is end;
architecture test of tb_mux_8to1 is
  signal a,b,c,d,e,f,g,h,s2,s1,s0,y : std_logic;
  constant data : std_logic_vector(7 downto 0) := "01001101";
begin
  dut : entity work.mux_8to1 port map (a,b,c,d,e,f,g,h,s2,s1,s0,y);
  a <= data(0); b <= data(1); c <= data(2); d <= data(3);
  e <= data(4); f <= data(5); g <= data(6); h <= data(7);
  process
    variable sel : std_logic_vector(2 downto 0);
  begin
    for i in 0 to 7 loop
      sel := std_logic_vector(to_unsigned(i,3));
      s2 <= sel(2); s1 <= sel(1); s0 <= sel(0);
      wait for 1 ns;
      assert y = data(i) severity failure;
    end loop;
    report "PASS tb_mux_8to1";
    stop;
    wait;
  end process;
end;
