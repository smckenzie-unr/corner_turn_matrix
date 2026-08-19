#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pytest
import subprocess
from pathlib import Path
from cocotb_tools.runner import get_runner

# Add the mcode GHDL path
os.environ["PATH"] = "/usr/bin:" + os.environ["PATH"]

# Add the Questa VSim path
os.environ["PATH"] = "/home/slmckenzie/intelFPGA_lite/24.1std/questa_fse/bin:/usr/bin:" + os.environ["PATH"]

# Set Questa license environment
os.environ["LM_LICENSE_FILE"] = "/home/slmckenzie/intelFPGA_lite/LR-275828_License.dat"

@pytest.mark.input_column_counter
def test_input_column_counter() -> None:
    toplevel_entity = "input_address_counter"
    testbench = "input_address_counter_tb"

    runner = get_runner("ghdl")

    runner.build(
        sources = [
            "./includes/ctm_package.vhd",
            f"./sources/{toplevel_entity}.vhd"
        ],
        build_dir = "./build/",
        hdl_toplevel = toplevel_entity,
        build_args = [
            "--std=08"
        ],
        parameters = {
            "C_NUM_COLS"       : 2048,
            "C_ADDRESS_WIDTH"  : 32,
            "C_BASE_ADDRESS"   : 0,
            "C_OFFSET_ADDRESS" : 4096
        },
        timescale = ("1ns", "1ps"),
        hdl_library = "work",
        always = True
    )

    runner.test(
        hdl_toplevel = toplevel_entity,
        test_module = testbench,
        hdl_toplevel_library = "work",
        hdl_toplevel_lang = "vhdl",
        test_args = [
            "--std=08",
            "--time-resolution=ps",
        ],
        plusargs = [
            "--stop-time=100us",
            "--ieee-asserts=disable-at-0"
        ],
        timescale = ("1ns", "1ps"),
        verbose = True,
        waves = True
    )

# @pytest.mark.input_column_counter
# def test_input_column_counter() -> None:
#     toplevel_entity = "input_address_counter"
#     testbench = "input_address_counter_tb"
    

#     #runner = get_runner("ghdl")
#     runner = get_runner("questa")

#     runner.build(
#         sources = [
#             "./includes/ctm_package.vhd",
#             f"./sources/{toplevel_entity}.vhd"
#         ],
#         build_dir = "./build/",
#         hdl_toplevel = toplevel_entity,
#         build_args = [
#             # "--std=08"
#             "-2008"
#         ],
#         parameters = {
#             "C_NUM_COLS"       : 2048,
#             "C_ADDRESS_WIDTH"  : 32,
#             "C_BASE_ADDRESS"   : 0,
#             "C_OFFSET_ADDRESS" : 4096
#         },
#         timescale = ("1ns", "1ps"),
#         hdl_library = "work",
#         always = True
#     )

#     runner.test(
#         hdl_toplevel = toplevel_entity,
#         test_module = testbench,
#         hdl_toplevel_library = "work",
#         hdl_toplevel_lang = "vhdl",
#         # test_args = [
#         #     # "--std=08",
#         #     # "--time-resolution=ps",
#         #     # "-2008"
#         # ],
#         plusargs = [
#             "-t",
#             "ps"
#             # "--stop-time=100us",
#             # "--ieee-asserts=disable-at-0"
#             # "-timescale"
#             # "+stop+100us"
#         ],
#         timescale = ("1ns", "1ps"),
#         verbose = True,
#         waves = True
#     )

@pytest.mark.xilinx_tdpram_wrapper
def test_input_column_counter() -> None:
    toplevel_entity = "xilinx_tdpram_wrapper"
    testbench = "tdpram_tb"
    os.makedirs("./build/work", exist_ok=True)
    # subprocess.run(["vmap", "xpm", "./questa_libs/xpm"])
    subprocess.run(
        ["vmap", "xpm", os.path.abspath("./questa_libs/xpm")],
        cwd="./build/work"
    )
    
    runner = get_runner("questa")

    runner.build(
        sources = [
            "./includes/ctm_package.vhd",
            f"./sources/{toplevel_entity}.vhd"
        ],
        build_dir = "./build/",
        hdl_toplevel = toplevel_entity,
        build_args = [
            "-2008",
        ],
        timescale = ("1ns", "1ps"),
        hdl_library = "work",
        always = True
    )

    runner.test(
        hdl_toplevel = toplevel_entity,
        test_module = testbench,
        hdl_toplevel_library = "work",
        hdl_toplevel_lang = "vhdl",
        plusargs = [
            "-L", 
            "xpm",
            "-t",
            "ps"
        ],
        timescale = ("1ns", "1ps"),
        verbose = True,
        waves = True
    )




# runner.build(
#     sources=[
#         "./includes/ctm_package.vhd",
#         f"./sources/{toplevel_entity}.vhd",

#         # XPM simulation models
#         "/opt/Xilinx/Vivado/2024.1/data/ip/xpm/xpm_VCOMP.vhd",
#         "/opt/Xilinx/Vivado/2024.1/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv",
#         "/opt/Xilinx/Vivado/2024.1/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv",
#         "/opt/Xilinx/Vivado/2024.1/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv",
#     ],
#     hdl_library="work",
#     build_dir="./build/",
#     build_args=[
#         "-2008",
#         "-L", "xpm"     # <-- IMPORTANT: tell Questa to link the XPM library
#     ],
#     always=True
# )
# runner.test(
#     hdl_toplevel=toplevel_entity,
#     test_module=testbench,
#     hdl_toplevel_library="work",
#     hdl_toplevel_lang="vhdl",
#     plusargs=[
#         "-L", "xpm",   # <-- REQUIRED for elaboration
#         "-t", "ps"
#     ],
#     waves=True,
#     verbose=True
# )
