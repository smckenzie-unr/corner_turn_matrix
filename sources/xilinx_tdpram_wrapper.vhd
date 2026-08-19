library ieee;
use ieee.std_logic_1164.all;

library xpm;
use xpm.vcomponents.all;

use work.ctm_package.all;

entity xilinx_tdpram_wrapper is
    generic (
        C_DATA_WIDTH       : integer range 8 to 64 := 16;
        C_MEMORY_DEPTH     : integer range 2 to 32768 := 2048;
        C_READ_A_LATENCY   : integer range 0 to 100 := 1;
        C_READ_B_LATENCY   : integer range 0 to 100 := 1;
        C_MEMORY_PRIMITIVE : string := "block";
        C_WRITE_MODE_A     : string := "no_change";
        C_WRITE_MODE_B     : string := "no_change";
        C_CLOCK_MODE       : string := "common_clock"
    );
    port (
        CLK_A      : in  std_logic;
        RST_A      : in  std_logic := '0';
        ENABLE_A   : in  std_logic := '0';
        WRITE_EN_A : in  std_logic_vector(C_DATA_WIDTH / 8 - 1 downto 0) := (others => '0');
        ADDRESS_A  : in  std_logic_vector(clog2(C_MEMORY_DEPTH) - 1 downto 0) := (others => '0');
        DATA_IN_A  : in  std_logic_vector(C_DATA_WIDTH - 1 downto 0) := (others => '0');
        DATA_OUT_A : out std_logic_vector(C_DATA_WIDTH - 1 downto 0);
        CLK_B      : in  std_logic := '0';
        RST_B      : in  std_logic := '0';
        ENABLE_B   : in  std_logic := '0';
        WRITE_EN_B : in  std_logic_vector(C_DATA_WIDTH / 8 - 1 downto 0) := (others => '0');
        ADDRESS_B  : in  std_logic_vector(clog2(C_MEMORY_DEPTH) - 1 downto 0) := (others => '0');
        DATA_IN_B  : in  std_logic_vector(C_DATA_WIDTH - 1 downto 0) := (others => '0');
        DATA_OUT_B : out std_logic_vector(C_DATA_WIDTH - 1 downto 0)
    );
end entity xilinx_tdpram_wrapper;

architecture synthesizable of xilinx_tdpram_wrapper is
    constant C_BYTE_WIDTH    : integer := 8;
    constant C_ADDRESS_WIDTH : integer := clog2(C_MEMORY_DEPTH);
    constant C_MEMORY_SIZE   : integer := C_DATA_WIDTH * C_MEMORY_DEPTH;
begin

    xpm_memory_tdpram_inst : xpm_memory_tdpram
        generic map (
            ADDR_WIDTH_A            => C_ADDRESS_WIDTH,
            ADDR_WIDTH_B            => C_ADDRESS_WIDTH,
            AUTO_SLEEP_TIME         => 0,
            BYTE_WRITE_WIDTH_A      => C_BYTE_WIDTH,
            BYTE_WRITE_WIDTH_B      => C_BYTE_WIDTH,
            CASCADE_HEIGHT          => 0,
            CLOCKING_MODE           => C_CLOCK_MODE,
            ECC_BIT_RANGE           => "7:0",
            ECC_MODE                => "no_ecc",
            ECC_TYPE                => "none",
            IGNORE_INIT_SYNTH       => 0,
            MEMORY_INIT_FILE        => "none",
            MEMORY_INIT_PARAM       => "0",
            MEMORY_OPTIMIZATION     => "true",
            MEMORY_PRIMITIVE        => C_MEMORY_PRIMITIVE,
            MEMORY_SIZE             => C_MEMORY_SIZE,
            MESSAGE_CONTROL         => 0,
            RAM_DECOMP              => "auto",
            READ_DATA_WIDTH_A       => C_DATA_WIDTH,
            READ_DATA_WIDTH_B       => C_DATA_WIDTH,
            READ_LATENCY_A          => C_READ_A_LATENCY,
            READ_LATENCY_B          => C_READ_B_LATENCY,
            READ_RESET_VALUE_A      => "0",
            READ_RESET_VALUE_B      => "0",
            RST_MODE_A              => "SYNC",
            RST_MODE_B              => "SYNC",
            SIM_ASSERT_CHK          => 1,
            USE_EMBEDDED_CONSTRAINT => 0,
            USE_MEM_INIT            => 0,
            USE_MEM_INIT_MMI        => 0,
            WAKEUP_TIME             => "disable_sleep",
            WRITE_DATA_WIDTH_A      => C_DATA_WIDTH,
            WRITE_DATA_WIDTH_B      => C_DATA_WIDTH,
            WRITE_MODE_A            => C_WRITE_MODE_A,
            WRITE_MODE_B            => C_WRITE_MODE_B,
            WRITE_PROTECT           => 0
        )
        port map (
            sleep          => '0',
            clka           => CLK_A,
            rsta           => RST_A,
            ena            => ENABLE_A,
            regcea         => '1',
            wea            => WRITE_EN_A, 
            addra          => ADDRESS_A,
            dina           => DATA_IN_A,
            injectsbiterra => '0',
            injectdbiterra => '0',
            douta          => DATA_OUT_A,
            sbiterra       => open,
            dbiterra       => open,
            clkb           => CLK_B,
            rstb           => RST_B,
            enb            => ENABLE_B, 
            regceb         => '1', 
            web            => WRITE_EN_B,
            addrb          => ADDRESS_B,
            dinb           => DATA_IN_B, 
            injectsbiterrb => '0',
            injectdbiterrb => '0',
            doutb          => DATA_OUT_B, 
            sbiterrb       => open, 
            dbiterrb       => open 
        );

end architecture synthesizable;