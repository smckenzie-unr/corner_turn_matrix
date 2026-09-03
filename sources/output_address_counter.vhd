----------------------------------------------------------------------------------
-- Company:    LogiTech DSP
-- Engineer:   Scott L. McKenzie
-- 
-- Create Date:    2026-06-21 17:11:17
-- Design Name:    Output Address Counter
-- Module Name:    output_address_counter
-- Project Name:   Corner Turn Matrix
-- Target Devices: Zynq-7000, Zynq Ultrascale+
-- Tool Versions:  Vivado 2024.1
-- Description:    This module computers the row wise address for performing the transpose
-- 
-- Dependencies:   IEEE.std_logic_1164.all, IEEE.numeric_std.all
-- 
-- Revision:
-- Revision 2026-06-21 - slmckenzie - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use work.ctm_package.all;

entity output_address_counter is
    generic (
        C_NUM_ROWS       : integer;
        C_NUM_COLS       : integer;
        C_ADDRESS_WIDTH  : integer;
        C_BASE_ADDRESS   : integer;
        C_OFFSET_ADDRESS : integer;
        C_REGISTER_ADDR  : boolean := true
    );
    port (
        CLK       : in  std_logic;
        RST       : in  std_logic;
        ENABLE    : in  std_logic;
        ADDR_CHNG : out std_logic;
        ADDRESS   : out std_logic_vector(C_ADDRESS_WIDTH - 1 downto 0)
    );
end entity output_address_counter;

architecture synthesizable of output_address_counter is
    constant C_ROWS          : unsigned(C_ADDRESS_WIDTH - 1 downto 0) := to_unsigned(C_NUM_ROWS, C_ADDRESS_WIDTH);
    constant C_COLS          : unsigned(C_ADDRESS_WIDTH - 1 downto 0) := to_unsigned(C_NUM_COLS, C_ADDRESS_WIDTH);
    constant C_MAX_BASE_ADDR : unsigned(C_ADDRESS_WIDTH - 1 downto 0) := get_max_address(
                                                                            C_BASE_ADDRESS,
                                                                            C_NUM_COLS,
                                                                            C_NUM_ROWS,
                                                                            C_ADDRESS_WIDTH
                                                                        );
    constant C_MAX_OFFS_ADDR : unsigned(C_ADDRESS_WIDTH - 1 downto 0) := get_max_address(
                                                                            C_OFFSET_ADDRESS,
                                                                            C_NUM_COLS,
                                                                            C_NUM_ROWS,
                                                                            C_ADDRESS_WIDTH
                                                                        );

    signal current_count : unsigned(C_ADDRESS_WIDTH - 1 downto 0) := (others => '0');
    signal next_count    : unsigned(C_ADDRESS_WIDTH - 1 downto 0);
    signal load_count    : unsigned(C_ADDRESS_WIDTH - 1 downto 0);

    signal row_idx       : unsigned(C_ADDRESS_WIDTH - 1 downto 0); 
    signal reset_row     : std_logic;

    signal col_idx       : unsigned(C_ADDRESS_WIDTH - 1 downto 0);
    signal reset_col     : std_logic;
    signal col_strobe    : std_logic;
begin

    addr_output_reg_gen : if (C_REGISTER_ADDR) generate
        ADDRESS <= std_logic_vector(current_count);
    else generate
        ADDRESS <= std_logic_vector(next_count);
    end generate addr_output_reg_gen;

    ADDR_CHNG <= '1' when (col_strobe = '1' and col_idx = C_COLS - 1) else '0';

    comb_proc : process (all) is
    begin
        reset_row <= '1' when (RST = '1' or row_idx >= C_ROWS - 1) else '0';
        reset_col <= '1' when (RST = '1' or (col_idx >= C_COLS and reset_row = '1')) else '0';
        col_strobe <= '1' when (row_idx = C_ROWS - 2) else '0';
    end process comb_proc;

    row_count_proc : process (CLK) is
    begin
        if (rising_edge(CLK)) then
            if (reset_row = '1') then
                row_idx <= (others => '0');
            else
                if (ENABLE = '1') then
                    row_idx <= row_idx + 1;
                end if;
            end if;
        end if;
    end process row_count_proc;

    column_count_proc : process (CLK) is
    begin
        if (rising_edge(CLK)) then
            if (reset_col = '1') then
                col_idx <= (others => '0');
            else
                if (col_strobe = '1') then
                    col_idx <= col_idx + 1;
                end if;
            end if;
        end if;
    end process column_count_proc;

    next_addr_count_proc : process (CLK) is
    begin
        if (rising_edge(CLK)) then
            if (RST = '1') then
                next_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
            else
                if (ENABLE = '1') then
                    next_count <= next_count + C_COLS;
                    if (reset_row = '1' and reset_col = '0') then
                        next_count <= load_count + col_idx;
                    elsif (reset_row = '1' and reset_col = '1') then
                        next_count <= load_count;
                    end if;
                end if;
            end if;
        end if;
    end process next_addr_count_proc;

    output_register_gen : if (C_REGISTER_ADDR) generate
        curr_addr_count_proc : process (CLK) is 
        begin
            if (rising_edge(CLK)) then
                if (RST = '1') then
                    current_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                else
                    if (ENABLE = '1') then
                        current_count <= next_count;
                    end if;
                end if;
            end if;
        end process curr_addr_count_proc;

        load_address_proc : process (CLK) is
        begin
            if (rising_edge(CLK)) then
                if (RST = '1') then
                    load_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                else
                    if (current_count = C_MAX_BASE_ADDR - 1) then
                        load_count <= to_unsigned(C_OFFSET_ADDRESS, C_ADDRESS_WIDTH);
                    elsif (current_count = C_MAX_OFFS_ADDR - 1) then
                        load_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                    end if;
                end if;
            end if;
        end process load_address_proc;
    else generate
        load_address_proc : process (CLK) is
        begin
            if (rising_edge(CLK)) then
                if (RST = '1') then
                    load_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                else
                    if (next_count = C_MAX_BASE_ADDR - 1) then
                        load_count <= to_unsigned(C_OFFSET_ADDRESS, C_ADDRESS_WIDTH);
                    elsif (next_count = C_MAX_OFFS_ADDR - 1) then
                        load_count <= to_unsigned(C_BASE_ADDRESS, C_ADDRESS_WIDTH);
                    end if;
                end if;
            end if;
        end process load_address_proc;
    end generate output_register_gen;

end architecture synthesizable;