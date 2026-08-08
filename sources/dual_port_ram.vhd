library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity dual_port_ram is
    generic (
        C_ADDRESS_WIDTH : integer range 8 to 64 := 32;
        C_WORD_WIDTH    : integer range 8 to 64 := 16;
        C_MEM_DEPTH     : integer range 4 to 32768 := 1024
    );
    port (
        CLK_A     : in std_ulogic;
        EN_A      : in std_ulogic;
        WR_EN_A   : in std_ulogic;
        ADDRESS_A : in std_ulogic_vector(C_ADDRESS_WIDTH - 1 downto 0);
        DIN_A     : in std_ulogic_vector(C_WORD_WIDTH - 1 downto 0);
        DOUT_A    : out std_ulogic_vector(C_WORD_WIDTH - 1 downto 0);
        CLK_B     : in std_ulogic;
        EN_B      : in std_ulogic;
        WR_EN_B   : in std_ulogic;
        ADDRESS_B : in std_ulogic_vector(C_ADDRESS_WIDTH - 1 downto 0);
        DIN_B     : in std_ulogic_vector(C_WORD_WIDTH - 1 downto 0);
        DOUT_B    : out std_ulogic_vector(C_WORD_WIDTH - 1 downto 0)
    );
end entity dual_port_ram;

architecture synthesizable of dual_port_ram is
    package ram_pkg is new work.ram_package
        generic map (
            C_MEM_DEPTH => C_MEM_DEPTH,
            C_DATA_WIDTH => C_WORD_WIDTH
        );
    use ram_pkg.all;

    shared variable ram : ram_t;
begin
    
end architecture synthesizable;