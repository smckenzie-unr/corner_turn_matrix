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

entity input_column_counter is
    generic (
        C_COUNTER_WIDTH : integer := 12;
        C_MEM_SPACE     : integer := 2048
    );
    port (
        CLK    : in  std_ulogic;
        RST    : in  std_ulogic;
        ENABLE : in  std_ulogic;
        OFFSET : in  unsigned(C_COUNTER_WIDTH - 1 downto 0);
        COUNT  : out unsigned(C_COUNTER_WIDTH - 1 downto 0)
    );
end entity input_column_counter;

architecture synthesizable of input_column_counter is
    signal counter       : unsigned(C_COUNTER_WIDTH - 1 downto 0);
    signal counter_reset : std_ulogic;

    attribute use_dsp : string;
    attribute use_dsp of counter : signal is "yes";
begin
    COUNT <= counter;
    
    comb_proc : process (all) is
        variable counter_stop  : unsigned(C_COUNTER_WIDTH - 1 downto 0);
    begin
        counter_stop := OFFSET + to_unsigned(C_MEM_SPACE, C_COUNTER_WIDTH) - 1;
        if ((RST = '1') or (counter >= counter_stop)) then
            counter_reset <= '1';
        else
            counter_reset <= '0';
        end if;
    end process comb_proc;

    counter_proc : process (CLK) is
    begin
        if rising_edge(CLK) then
            if (counter_reset = '1') then
                counter <= OFFSET;
            elsif (ENABLE = '1') then
                counter <= counter + 1;
            end if;
        end if;
    end process;
end architecture synthesizable;