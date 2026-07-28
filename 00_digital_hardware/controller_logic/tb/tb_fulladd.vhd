library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity tb_fulladd is end;
architecture test of tb_fulladd is
  signal a, b, cin, s, cout : std_logic := '0';
begin
  dut : entity work.fulladd port map (a, b, cin, s, cout);
  process
    variable total : integer;
  begin
    for av in 0 to 1 loop
      for bv in 0 to 1 loop
        for cv in 0 to 1 loop
          a <= std_logic'val(av + 2);
          b <= std_logic'val(bv + 2);
          cin <= std_logic'val(cv + 2);
          wait for 1 ns;
          total := av + bv + cv;
          assert s = std_logic'val((total mod 2) + 2) severity failure;
          assert cout = std_logic'val((total / 2) + 2) severity failure;
        end loop;
      end loop;
    end loop;
    report "PASS tb_fulladd";
    stop;
    wait;
  end process;
end;
