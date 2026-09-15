library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity address_logic is
    port (
        CLK           : in  std_logic;
        RST           : in  std_logic;
        INPUT_CHANGE  : in  std_logic;
        OUTPUT_CHANGE : in  std_logic;
        INPUT_ENABLE  : out std_logic;
        OUTPUT_ENABLE : out std_logic;
        FIRST_PASS_EN : out std_logic
    );
end entity address_logic;

architecture synthesizable of address_logic is
    signal input_chng_detect : std_logic;
    signal output_chng_detect : std_logic;

    signal state_change : std_logic;

    signal first_pass_detect : std_logic;
begin

    OUTPUT_ENABLE <= not output_chng_detect;
    INPUT_ENABLE <= not input_chng_detect;
    FIRST_PASS_EN <= first_pass_detect;

    first_write_proc : process(CLK) is 
    begin
        if (rising_edge(CLK)) then
            if (RST = '1') then
                first_pass_detect <= '0';
            elsif (input_chng_detect = '1') then
                first_pass_detect <= '1';
            end if;
        end if;
    end process first_write_proc;

    in_flip_latch : process(CLK) is
    begin
        if (rising_edge(CLK)) then
            if (RST = '1' or state_change = '1') then
                input_chng_detect <= '0';
            elsif (INPUT_CHANGE = '1') then
                input_chng_detect <= '1';
            end if;
        end if;
    end process in_flip_latch;

    out_flip_latch : process(CLK) is
    begin
        if (rising_edge(CLK)) then
            if (RST = '1' or state_change = '1') then
                output_chng_detect <= '0';
            elsif (OUTPUT_CHANGE = '1') then
                output_chng_detect <= '1';
            end if;
        end if;
    end process out_flip_latch;

    state_combination : process(all) is
    begin
        state_change <= '0';
        if (input_chng_detect = '1' and output_chng_detect = '1') then
            state_change <= '1';
        end if;
    end process state_combination;
end architecture synthesizable;