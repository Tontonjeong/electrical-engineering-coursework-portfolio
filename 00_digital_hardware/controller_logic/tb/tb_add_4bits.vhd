library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;

entity tb_add_4bits is end;
architecture test of tb_add_4bits is
  signal a, b, sum : std_logic_vector(3 downto 0);
  signal cin, cout : std_logic;
begin
  dut : entity work.add_4bits port map (a, b, cin, sum, cout);
  process
    variable total : integer;
  begin
    for av in 0 to 15 loop
      for bv in 0 to 15 loop
        for cv in 0 to 1 loop
          a <= std_logic_vector(to_unsigned(av, 4));
          b <= std_logic_vector(to_unsigned(bv, 4));
          if cv = 0 then cin <= '0'; else cin <= '1'; end if;
          wait for 1 ns;
          total := av + bv + cv;
          assert unsigned(sum) = to_unsigned(total mod 16, 4) severity failure;
          if total >= 16 then
            assert cout = '1' severity failure;
          else
            assert cout = '0' severity failure;
          end if;
        end loop;
      end loop;
    end loop;
    report "PASS tb_add_4bits";
    stop;
    wait;
  end process;
end;
