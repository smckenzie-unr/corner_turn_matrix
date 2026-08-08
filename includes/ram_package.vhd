library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package ram_package is
    generic (
        C_MEM_DEPTH  : integer range 4 to 32768 := 1024;
        C_DATA_WIDTH : integer range 8 to 64 := 32
    );

    type reg_array is array (natural range <>) of std_ulogic_vector;

    type ram_t is protected
        procedure write(addr : unsigned; data : std_ulogic_vector);
        impure function read(addr : unsigned) return std_ulogic_vector;
    end protected ram_t;
end package ram_package;

package body ram_package is
    type ram_t is protected body
        variable mem : reg_array(0 to C_MEM_DEPTH - 1)(C_DATA_WIDTH - 1 downto 0);

        procedure write(addr : unsigned; data : std_ulogic_vector) is
        begin
            mem(to_integer(addr)) := data;
        end procedure;

        impure function read(addr : unsigned) return std_ulogic_vector is
        begin
            return mem(to_integer(addr));
        end function;
    end protected body ram_t;
end package body ram_package;