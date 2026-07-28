library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity tb_dec_3to8 is end;
architecture test of tb_dec_3to8 is
  signal d2, d1, d0 : std_logic;
  signal y : std_logic_vector(7 downto 0);
begin
  dut : entity work.dec_3to8
    port map (d2, d1, d0, y(0), y(1), y(2), y(3), y(4), y(5), y(6), y(7));
  process
    variable sel : std_logic_vector(2 downto 0);
  begin
    for i in 0 to 7 loop
      sel := std_logic_vector(to_unsigned(i, 3));
      d2 <= sel(2); d1 <= sel(1); d0 <= sel(0);
      wait for 1 ns;
      assert unsigned(y) = shift_left(to_unsigned(1, 8), i) severity failure;
    end loop;
    report "PASS tb_dec_3to8";
    stop;
    wait;
  end process;
end;
