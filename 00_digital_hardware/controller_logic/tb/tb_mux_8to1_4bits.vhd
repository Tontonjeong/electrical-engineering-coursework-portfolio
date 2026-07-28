library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity tb_mux_8to1_4bits is end;
architecture test of tb_mux_8to1_4bits is
  signal a,b,c,d,e,f,g,h,y : std_logic_vector(3 downto 0);
  signal s2,s1,s0 : std_logic;
begin
  dut : entity work.mux_8to1_4bits port map (a,b,c,d,e,f,g,h,s2,s1,s0,y);
  a<="0000"; b<="0001"; c<="0010"; d<="0011";
  e<="0100"; f<="0101"; g<="0110"; h<="0111";
  process
    variable sel : std_logic_vector(2 downto 0);
  begin
    for i in 0 to 7 loop
      sel := std_logic_vector(to_unsigned(i,3));
      s2 <= sel(2); s1 <= sel(1); s0 <= sel(0);
      wait for 1 ns;
      assert unsigned(y) = to_unsigned(i,4) severity failure;
    end loop;
    report "PASS tb_mux_8to1_4bits";
    stop;
    wait;
  end process;
end;
