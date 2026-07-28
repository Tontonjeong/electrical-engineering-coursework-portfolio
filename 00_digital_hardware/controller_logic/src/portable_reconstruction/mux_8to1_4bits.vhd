-- Portfolio reconstruction from the supplied assignment specification.
library ieee;
use ieee.std_logic_1164.all;

entity mux_8to1_4bits is
  port (
    a, b, c, d, e, f, g, h : in  std_logic_vector(3 downto 0);
    s2, s1, s0             : in  std_logic;
    y                       : out std_logic_vector(3 downto 0)
  );
end entity;

architecture structural of mux_8to1_4bits is
  component mux_8to1 is
    port (
      a, b, c, d, e, f, g, h : in std_logic;
      s2, s1, s0 : in std_logic;
      y : out std_logic
    );
  end component;
begin
  gen_bits : for i in 0 to 3 generate
    u_mux : mux_8to1
      port map (
        a => a(i), b => b(i), c => c(i), d => d(i),
        e => e(i), f => f(i), g => g(i), h => h(i),
        s2 => s2, s1 => s1, s0 => s0, y => y(i)
      );
  end generate;
end architecture;
