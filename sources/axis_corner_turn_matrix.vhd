library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_misc.all;

use work.ctm_package.all;

entity axis_corner_turn_matrix is
    generic (
        C_NUMBER_ROWS : positive;
        C_NUMBER_COLS : positive;
        C_DATA_WIDTH  : integer range 8 to 1204
    );
    port (
        AXIS_ACLK     : in  std_logic;
        AXIS_ARSTN    : in  std_logic;
        S_AXIS_TVALID : in  std_logic;
        S_AXIS_TREADY : out std_logic;
        S_AXIS_TDATA  : in  std_logic_vector(C_DATA_WIDTH - 1 downto 0);
        M_AXIS_TVALID : out std_logic;
        M_AXIS_TREADY : in  std_logic;
        M_AXIS_TDATA  : out std_logic_vector(C_DATA_WIDTH - 1 downto 0)
    );
end entity axis_corner_turn_matrix;

architecture synthesizable of axis_corner_turn_matrix is
    constant C_BUFFER_SIZE    : integer := 256;
    constant C_TOTAL_MEM_SIZE : integer := C_BUFFER_SIZE + 2 * C_NUMBER_COLS * C_NUMBER_ROWS;
    constant C_ADDRESS_SIZE   : integer := clog2(C_TOTAL_MEM_SIZE);

    type state_machine_t is (IDLE, BUFF_ONE, BUFF_TWO, RESET);

    signal tdpram_reset       : std_logic;
    signal tdpram_input_en    : std_logic_vector(C_DATA_WIDTH / 8 - 1 downto 0);
    signal input_count_en     : std_logic;
    signal tdpram_input_addr  : std_logic_vector(C_ADDRESS_SIZE - 1 downto 0);

    signal tdpram_output_en   : std_logic;
    signal tdpram_output_addr : std_logic_vector(C_ADDRESS_SIZE - 1 downto 0);

    signal master_tready      : std_logic;

    signal curr_out_state     : state_machine_t;
    signal next_out_state     : state_machine_t;

    signal curr_in_state      : state_machine_t;
    signal next_in_state      : state_machine_t;
begin

    tdpram_reset <= not AXIS_ARSTN;
    input_count_en <= or_reduce(tdpram_input_en);

    MEM : entity work.xilinx_tdpram_wrapper
        generic map (
            C_DATA_WIDTH   => C_DATA_WIDTH,
            C_MEMORY_DEPTH => C_TOTAL_MEM_SIZE
        )
        port map (
            CLK_A      => AXIS_ACLK,
            RST_A      => tdpram_reset,
            WRITE_EN_A => tdpram_input_en,
            ADDRESS_A  => tdpram_input_addr,
            DATA_IN_A  => S_AXIS_TDATA,
            DATA_OUT_A => open,
            RST_B      => tdpram_reset,
            ENABLE_B   => tdpram_output_en,
            ADDRESS_B  => tdpram_output_addr,
            DATA_OUT_B => M_AXIS_TDATA
        );

    INPUT_CTRL : entity work.input_address_counter
        generic map (
            C_NUM_COLS       => C_NUMBER_ROWS * C_NUMBER_COLS,
            C_ADDRESS_WIDTH  => C_ADDRESS_SIZE,
            C_BASE_ADDRESS   => 0,
            C_OFFSET_ADDRESS => C_TOTAL_MEM_SIZE / 2
        )
        port map (
            CLK     => AXIS_ACLK,
            RST     => tdpram_reset,
            ENABLE  => input_count_en,
            ADDRESS => unsigned(tdpram_input_addr)
        );

    OUTPUT_CTRL : entity work.output_address_counter
        generic map (
            C_NUM_ROWS       => C_NUMBER_ROWS,
            C_NUM_COLS       => C_NUMBER_COLS,
            C_ADDRESS_WIDTH  => C_ADDRESS_SIZE,
            C_BASE_ADDRESS   => 0,
            C_OFFSET_ADDRESS => C_TOTAL_MEM_SIZE / 2
        )
        port map (
            CLK     => AXIS_ACLK,
            RST     => tdpram_reset,
            ENABLE  => tdpram_output_en,
            ADDRESS => tdpram_input_addr
        );

    curr_state_proc : process(AXIS_ACLK) is
    begin
        if (rising_edge(AXIS_ACLK)) then
            if (AXIS_ARSTN = '0') then
                curr_out_state <= RESET;
                curr_in_state <= RESET;
            else
                curr_out_state <= next_out_state;
                curr_in_state <= next_in_state;
            end if;
        end if;
    end process curr_state_proc;

    output_comb_proc : process(all) is
    begin
        
    end process output_comb_proc;

end architecture synthesizable;