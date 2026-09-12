library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity address_logic is
    port (
        CLK           : in  std_logic;
        RST           : in  std_logic;
        INPUT_CHANGE  : in  std_logic;
        OUTPUT_CHANGE : in  std_logic;
        DATA_VALID    : in  std_logic;
        DATA_READY    : in  std_logic;
        INPUT_ENABLE  : out std_logic;
        OUTPUT_ENABLE : out std_logic
    );
end entity address_logic;

architecture synthesizable of address_logic is
    type operational_state is (FILL0_DRAIN1, FILL1_DRAIN0, RESET);

    signal curr_state : operational_state;
    signal next_state : operational_state;

    signal input_chng_detect : std_logic;
    signal output_chng_detect : std_logic;

    signal state_change : std_logic;
begin

    OUTPUT_ENABLE <= DATA_READY and not output_chng_detect;
    INPUT_ENABLE <= DATA_VALID and not input_chng_detect;

    state_process : process(CLK) is
    begin
        if (rising_edge(CLK)) then
            if (RST = '1') then
                curr_state <= RESET;
            else
                curr_state <= next_state;
            end if;
        end if;
    end process state_process;

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
        next_state <= curr_state;
        state_change <= '0';
        case curr_state is
            when RESET =>
                next_state <= FILL0_DRAIN1;
            when FILL0_DRAIN1 =>
                if (input_chng_detect = '1' and output_chng_detect = '1') then
                    next_state <= FILL1_DRAIN0;
                    state_change <= '1';
                else
                    next_state <= FILL0_DRAIN1;
                end if;
            when FILL1_DRAIN0 =>
                if (input_chng_detect = '1' and output_chng_detect = '1') then
                    next_state <= FILL0_DRAIN1;
                    state_change <= '1';
                else
                    next_state <= FILL1_DRAIN0;
                end if;
            when others =>
                null;
        end case;
    end process state_combination;
end architecture synthesizable;