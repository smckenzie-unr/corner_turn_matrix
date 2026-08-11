----------------------------------------------------------------------------------
-- Company:    LogiTech DSP
-- Engineer:   Scott L. McKenzie
-- 
-- Create Date:    2026-06-14 15:34:55
-- Design Name:    Corner Turn Matrix
-- Module Name:    input_column_counter
-- Project Name:   RADAR FPGA DSP
-- Target Devices: Zynq-7000, Zynq Ultrascale
-- Tool Versions:  Vivado 2024.1
-- Description:    This module is the input column counter for the TDPRAM addrb port. This will 
--                 increment the column address for each input sample, facilitating the corner 
--                 turn operation in the matrix.
--
-- 
-- Dependencies: IEEE.std_logic_1164, IEEE.numeric_std  
-- 
-- Revision:
-- Revision 2026-06-14 - slmckenzie - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.ctm_package.all;

entity input_address_counter is
    generic (
        C_NUM_COLS       : integer;
        C_ADDRESS_WIDTH  : integer;
        C_BASE_ADDRESS   : integer;
        C_OFFSET_ADDRESS : integer
    );
    port (
        CLK     : in  std_ulogic;
        RST     : in  std_ulogic;
        ENABLE  : in  std_ulogic;
        ADDRESS : out unsigned(C_ADDRESS_WIDTH - 1 downto 0)
    );
end entity input_address_counter;

architecture synthesizable of input_address_counter is
    constant C_MAX_BASE_ADDR : unsigned := get_max_address(
                                                C_BASE_ADDRESS,
                                                C_NUM_COLS,
                                                1,
                                                C_ADDRESS_WIDTH
                                            );
    constant C_MAX_OFFS_ADDR : unsigned := get_max_address(
                                                C_OFFSET_ADDRESS,
                                                C_NUM_COLS,
                                                1,
                                                C_ADDRESS_WIDTH
                                            );

    signal counter       : unsigned(C_ADDRESS_WIDTH - 1 downto 0);
    signal counter_strb  : std_ulogic;
    signal load_count    : unsigned(C_ADDRESS_WIDTH - 1 downto 0);
begin
    ADDRESS <= counter;

    counter_proc : process (CLK) is
    begin
        if rising_edge(CLK) then
            if (RST = '1') then
                counter <= (others => '0');
            elsif (counter_strb = '1') then
                counter <= load_count;
            else 
                if (ENABLE = '1') then
                    counter <= counter + 1;
                end if;
            end if;
        end if;
    end process;

    load_address_proc : process (CLK) is
    begin
        if (rising_edge(CLK)) then
            if (RST = '1') then
                load_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                counter_strb <= '0';
            else
                counter_strb <= '0';
                if (counter = C_MAX_BASE_ADDR - 1) then
                    counter_strb <= '1';
                    load_count <= to_unsigned(C_OFFSET_ADDRESS, C_ADDRESS_WIDTH);
                elsif (counter = C_MAX_OFFS_ADDR - 1) then
                    counter_strb <= '1';
                    load_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                end if;
            end if;
        end if;
    end process load_address_proc;
end architecture synthesizable;