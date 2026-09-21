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
    constant C_COUNTER_SIZE   : integer := 2;

    type state_machine_t is (BUFF_ONE, BUFF_TWO, RESET);

    signal tdpram_reset       : std_logic;
    signal tdpram_input_en    : std_logic_vector(C_DATA_WIDTH / 8 - 1 downto 0);
    signal input_count_en     : std_logic;
    signal tdpram_input_addr  : unsigned(C_ADDRESS_SIZE - 1 downto 0);

    signal tdpram_output_en   : std_logic;
    signal tdpram_output_addr : std_logic_vector(C_ADDRESS_SIZE - 1 downto 0);

    signal input_flip         : std_logic;
    signal output_flip        : std_logic;

    signal axis_tready        : std_logic;
    signal axis_tvalid        : std_logic;
    signal tvalid_notify      : std_logic;

    signal beat_counter       : unsigned(C_COUNTER_SIZE - 1 downto 0);
begin

    S_AXIS_TREADY <= axis_tready;
    M_AXIS_TVALID <= axis_tvalid;

    tdpram_reset <= not AXIS_ARSTN;
    tdpram_input_en <= (others => input_count_en);

    tvalid_notify <= '1' when (beat_counter > 0) else '0';
    axis_tready <= '1' when (beat_counter < 2) else '0';

    tvalid_proc : process(AXIS_ACLK) is
    begin
        if (rising_edge(AXIS_ACLK)) then
            if (AXIS_ARSTN = '0') then
                axis_tvalid <= '0';
            elsif (tvalid_notify = '1') then
                axis_tvalid <= '1';
            else
                axis_tvalid <= '0';
            end if;
        end if;
    end process tvalid_proc;

    combination_proc : process(all) is
    begin
        if (S_AXIS_TVALID = '1' and axis_tready = '1') then
            input_count_en <= '1';
        else 
            input_count_en <= '0';
        end if;

        if(tvalid_notify = '1' and M_AXIS_TREADY = '1') then
            tdpram_output_en <= '1';
        else
            tdpram_output_en <= '0';
        end if;
    end process combination_proc;

    counter_proc : process(AXIS_ACLK) is
    begin
        if (rising_edge(AXIS_ACLK)) then
            if (AXIS_ARSTN = '0') then
                beat_counter <= (others => '0');
            elsif (input_flip = '1') then
                beat_counter <= beat_counter + 1;
            elsif (output_flip = '1') then
                beat_counter <= beat_counter - 1;
            end if;
        end if;
    end process counter_proc;

    MEM : entity work.xilinx_tdpram_wrapper
        generic map (
            C_DATA_WIDTH   => C_DATA_WIDTH,
            C_MEMORY_DEPTH => C_TOTAL_MEM_SIZE
        )
        port map (
            CLK_A      => AXIS_ACLK,
            RST_A      => tdpram_reset,
            WRITE_EN_A => tdpram_input_en,
            ADDRESS_A  => std_logic_vector(tdpram_input_addr),
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
            CLK       => AXIS_ACLK,
            RST       => tdpram_reset,
            ENABLE    => input_count_en,
            ADDR_CHNG => input_flip,
            ADDRESS   => tdpram_input_addr
        );

    OUTPUT_CTRL : entity work.output_address_counter
        generic map (
            C_NUM_ROWS       => C_NUMBER_ROWS,
            C_NUM_COLS       => C_NUMBER_COLS,
            C_ADDRESS_WIDTH  => C_ADDRESS_SIZE,
            C_BASE_ADDRESS   => 0,
            C_OFFSET_ADDRESS => C_TOTAL_MEM_SIZE / 2,
            C_REGISTER_ADDR  => false
        )
        port map (
            CLK       => AXIS_ACLK,
            RST       => tdpram_reset,
            ENABLE    => tdpram_output_en,
            ADDR_CHNG => output_flip,
            ADDRESS   => tdpram_output_addr
        );

end architecture synthesizable;