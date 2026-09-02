#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pytest
import subprocess
from pathlib import Path
from cocotb_tools.runner import get_runner, VHDL, Verilog
from pytest import FixtureRequest

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
            VHDL("./includes/ctm_package.vhd"),
            VHDL(f"./sources/{toplevel_entity}.vhd")
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

@pytest.mark.output_column_counter
def test_output_column_counter() -> None:
    toplevel_entity = "output_address_counter"
    testbench = "output_address_counter_tb"

    runner = get_runner("ghdl")

    runner.build(
        sources = [
            VHDL("./includes/ctm_package.vhd"),
            VHDL(f"./sources/{toplevel_entity}.vhd")
        ],
        build_dir = "./build/",
        hdl_toplevel = toplevel_entity,
        build_args = [
            "--std=08"
        ],
        parameters = {
            "C_NUM_ROWS"       : 32,
            "C_NUM_COLS"       : 128,
            "C_ADDRESS_WIDTH"  : 32,
            "C_BASE_ADDRESS"   : 0,
            "C_OFFSET_ADDRESS" : 8192,
            "C_REGISTER_ADDR"  : "true"
        },
        timescale = ("1ns", "1fs"),
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
           "--time-resolution=fs",
        ],
        plusargs = [
            "--stop-time=100us",
            "--ieee-asserts=disable-at-0"
        ],
        timescale = ("1ns", "1fs"),
        verbose = True,
        waves = True
    )

@pytest.mark.xilinx_tdpram_wrapper
def test_tdpram(request : FixtureRequest) -> None:
    toplevel_entity = "xilinx_tdpram_wrapper"
    testbench = "tdpram_tb"
    primitive = "block"

    match (primitive):
        case "block":
            testcase = "tdpram_bram_simulation"
            parameters = {
                "C_READ_A_LATENCY" : 1,
                "C_READ_B_LATENCY" : 1,
                "C_MEMORY_PRIMITIVE" : "block",
                "C_WRITE_MODE_A" : "no_change",
                "C_WRITE_MODE_B" : "no_change",
            }
        case "distribuited":
            testcase = "tdpram_distributed_simulation",
            parameters = {
                "C_READ_A_LATENCY" : 0,
                "C_READ_B_LATENCY" : 0,
                "C_MEMORY_PRIMITIVE" : "distributed",
                "C_WRITE_MODE_A" : "read_first",
                "C_WRITE_MODE_B" : "read_first",
            },
        case _:
            testcase = "tdpram_bram_simulation"
            parameters = {
                "C_READ_A_LATENCY" : 1,
                "C_READ_B_LATENCY" : 1,
                "C_MEMORY_PRIMITIVE" : "block",
                "C_WRITE_MODE_A" : "no_change",
                "C_WRITE_MODE_B" : "no_change",
            }
    
    runner = get_runner("questa")

    runner.build(
        sources = [
            Verilog("/tools/Xilinx/Vivado/2024.1/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv")
        ],
        build_args = ["-quiet"],
        build_dir = "./build/",
        timescale = ("1ns", "1ps"),
        hdl_library = "work",
        always = True
    )

    runner.build(
        sources = [
            VHDL("/tools/Xilinx/Vivado/2024.1/data/ip/xpm/xpm_VCOMP.vhd")
        ],
        build_dir = "./build/",
        timescale = ("1ns", "1ps"),
        hdl_library = "xpm",
        always = True
    )

    runner.build(
        sources = [
            VHDL("./includes/ctm_package.vhd"),
            VHDL(f"./sources/{toplevel_entity}.vhd")
        ],
        build_dir = "./build/",
        hdl_toplevel = toplevel_entity,
        build_args = [
            VHDL("-2008"),
            Verilog("-L"),
            Verilog("xpm"),
            "-quiet"
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
            "ps",
            "-quiet"
        ],
        testcase = testcase,
        parameters = parameters,
        timescale = ("1ns", "1ps"),
        verbose = False,
        waves = True
    )