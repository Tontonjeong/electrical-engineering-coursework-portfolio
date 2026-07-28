-- Portfolio reconstruction from the supplied assignment specification.
-- The original decoder source was referenced by the recovered mux project but
-- was not present in the archive. This file is not presented as recovered work.
library ieee;
use ieee.std_logic_1164.all;

entity dec_3to8 is
  port (
    d2, d1, d0 : in  std_logic;
    y0, y1, y2, y3, y4, y5, y6, y7 : out std_logic
  );
end entity;

architecture rtl of dec_3to8 is
  signal sel : std_logic_vector(2 downto 0);
  signal y   : std_logic_vector(7 downto 0);
begin
  sel <= d2 & d1 & d0;
  with sel select
    y <= "00000001" when "000",
         "00000010" when "001",
         "00000100" when "010",
         "00001000" when "011",
         "00010000" when "100",
         "00100000" when "101",
         "01000000" when "110",
         "10000000" when "111",
         "00000000" when others;
  y0 <= y(0);
  y1 <= y(1);
  y2 <= y(2);
  y3 <= y(3);
  y4 <= y(4);
  y5 <= y(5);
  y6 <= y(6);
  y7 <= y(7);
end architecture;
