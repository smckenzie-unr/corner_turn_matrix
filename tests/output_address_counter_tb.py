#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import cocotb
import random
import numpy as np
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles
from cocotb.handle import HierarchyObject, SimHandleBase

from scripts.tb_utils import setup_clock

logger = logging.getLogger("output_column_counter_tb")
logger.setLevel(logging.INFO)
logger.propagate = True

@cocotb.test()
async def constant_enable(DUT : HierarchyObject) -> None:
    logger.info(f"{'*'*33} Starting constant enable test {'*'*34}")
    DUT.RST.value = 1
    DUT.ENABLE.value = 0

    num_cols = int(DUT.C_NUM_COLS.value)
    num_rows = int(DUT.C_NUM_ROWS.value)
    base = int(DUT.C_BASE_ADDRESS.value)
    offset = int(DUT.C_OFFSET_ADDRESS.value)
    logger.info(f"Testing Number of columns: {num_cols}")
    logger.info(f"Testing Number of rows: {num_rows}")
    logger.info(f"Base Address: 0x{base:08X}")
    logger.info(f"offset Address: 0x{offset:08X}")

    logger.info("Starting clock at 325 MHz")
    await setup_clock(DUT.CLK, 320e6)
    await Timer(1, unit = "us")

    base_addresses = [int(DUT.C_BASE_ADDRESS.value), int(DUT.C_OFFSET_ADDRESS.value)]
    count_check = 0
    pass_count = 0

    logger.info("Deasserting reset")
    DUT.RST.value = 0
    await Timer(1, unit = "us")

    await RisingEdge(DUT.CLK)
    DUT.ENABLE.value = 1
    if (DUT.C_REGISTER_ADDR.value):
        await RisingEdge(DUT.CLK)
    for addr in base_addresses:
        for c in range(0, num_cols, 1):
            for r in range(0, num_rows, 1):
                count_check = r * num_cols + c + addr
                await RisingEdge(DUT.CLK)
                logger.debug(f"{count_check} : {int(DUT.ADDRESS.value)}")
                if (int(DUT.ADDRESS.value) == count_check):
                    pass_count += 1

    assert (pass_count == 2 * num_cols * num_rows), \
        "FAILURE. PASS COUNT WAS NOT EQUAL TO 2 * NUM_COLS * NUM_ROWS"

    await RisingEdge(DUT.CLK)
    DUT.ENABLE.value = 0
    
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return