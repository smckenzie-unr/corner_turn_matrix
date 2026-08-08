library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.math_real.all;

package ctm_package is
    pure function get_max_address(
        base_addr  : integer;
        num_cols   : integer;
        num_rows   : integer;
        addr_width : integer
    ) return unsigned;

    pure function clog2(n : integer) return integer;
    pure function clog2(n : real) return real;
end package ctm_package;


package body ctm_package is
    pure function get_max_address(
        base_addr  : integer;
        num_cols   : integer;
        num_rows   : integer;
        addr_width : integer
    ) return unsigned is
        variable num_elements : integer := 0;
        variable sum_addr     : integer := 0;
    begin
        num_elements := num_cols * num_rows;
        sum_addr := base_addr + num_elements - 1;
        return to_unsigned(sum_addr, addr_width);
    end function get_max_address;
    
    pure function clog2(n : integer) return integer is
    begin
        return integer(ceil(log2(real(n))));
    end function clog2;

    pure function clog2(n : real) return real is
    begin
        return ceil(log2(n));
    end function clog2;
end package body;