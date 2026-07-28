-- Portfolio reconstruction from the supplied assignment specification.
-- The recovered material documented behavior and an archived waveform, but the
-- completed source was not present. Clear is implemented asynchronously here
-- and this assumption is explicitly excluded from claims about the old archive.
library ieee;
use ieee.std_logic_1164.all;

entity usr_4bit is
  port (
    clk, clear : in  std_logic;
    s          : in  std_logic_vector(1 downto 0);
    d_in       : in  std_logic;
    p_in       : in  std_logic_vector(3 downto 0);
    q          : out std_logic_vector(3 downto 0)
  );
end entity;

architecture rtl of usr_4bit is
  signal q_reg : std_logic_vector(3 downto 0) := "0001";
begin
  process (clk, clear)
  begin
    if clear = '1' then
      q_reg <= (others => '0');
    elsif rising_edge(clk) then
      case s is
        when "00" => q_reg <= q_reg;
        when "01" => q_reg <= d_in & q_reg(3 downto 1);
        when "10" => q_reg <= q_reg(2 downto 0) & d_in;
        when "11" => q_reg <= p_in;
        when others => q_reg <= q_reg;
      end case;
    end if;
  end process;
  q <= q_reg;
end architecture;
