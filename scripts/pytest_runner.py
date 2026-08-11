#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from cocotb_tools.runner import get_runner

os.environ["PATH"] = "/usr/bin:" + os.environ["PATH"]

def test_input_column_counter() -> None:
    toplevel_entity = "input_address_counter"
    testbench = "input_address_counter_tb"

    runner = get_runner("ghdl")

    runner.build(
        sources = [
            f"./sources/{toplevel_entity}.vhd",
            "./includes/ctm_package.vhd"
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