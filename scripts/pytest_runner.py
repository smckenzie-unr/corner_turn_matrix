#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from cocotb_tools.runner import get_runner

#os.environ["PATH"] = "/usr/bin:" + os.environ["PATH"]
os.environ["PATH"] = "/home/slmckenzie/intelFPGA_lite/24.1std/questa_fse/bin:/usr/bin:" + os.environ["PATH"]

# Set Questa license environment
os.environ["LM_LICENSE_FILE"] = "/home/slmckenzie/intelFPGA_lite/LR-275828_License.dat"

# Add workspace root to PYTHONPATH so cocotb can find the testbench
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

def test_input_column_counter() -> None:
    toplevel_entity = "input_address_counter"
    testbench = "input_address_counter_tb"

    #runner = get_runner("ghdl")
    runner = get_runner("questa")

    runner.build(
        sources = [
            "./includes/ctm_package.vhd",
            f"./sources/{toplevel_entity}.vhd"
        ],
        build_dir = "./build/",
        hdl_toplevel = toplevel_entity,
        build_args = [
            # "--std=08"
            "-2008"
        ],
        parameters = {
            "C_NUM_COLS"       : 2048,
            "C_ADDRESS_WIDTH"  : 32,
            "C_BASE_ADDRESS"   : 0,
            "C_OFFSET_ADDRESS" : 4096
        },
        timescale = ("1ns", "1ns"),
        hdl_library = "work",
        always = True
    )

    runner.test(
        hdl_toplevel = toplevel_entity,
        test_module = testbench,
        hdl_toplevel_library = "work",
        hdl_toplevel_lang = "vhdl",
        # test_args = [
        #     # "--std=08",
        #     # "--time-resolution=ps",
        #     # "-2008"
        # ],
        plusargs = [
            # "--stop-time=100us",
            # "--ieee-asserts=disable-at-0"
            "+stop+100us"
        ],
        timescale = ("1ns", "1ns"),
        verbose = True,
        waves = True
    )