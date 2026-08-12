#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import cocotb
import numpy as np
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from cocotb.handle import HierarchyObject, SimHandleBase

from scripts.tb_utils import setup_clock

logger = logging.getLogger("input_column_counter_tb")
logger.setLevel(logging.DEBUG)
logger.propagate = True

@cocotb.test()
async def constant_enable(DUT : HierarchyObject) -> None:
    logger.info(f"{'*'*33} Starting constant enable test {'*'*34}")
    DUT.RST.value = 1
    DUT.ENABLE.value = 0

    num_cols = int(DUT.C_NUM_COLS.value)
    base = int(DUT.C_BASE_ADDRESS.value)
    offset = int(DUT.C_OFFSET_ADDRESS.value)
    logger.info(f"Testing Number of columns: {num_cols}")
    logger.info(f"Base Address: 0x{base:08X}")
    logger.info(f"offset Address: 0x{offset:08X}")

    logger.info("Starting clock at 325 MHz")
    await setup_clock(DUT.CLK, 200e6)
    await Timer(1, unit = "us")

    logger.info("Deasserting reset")
    DUT.RST.value = 0
    await Timer(1, unit = "us")

    await RisingEdge(DUT.CLK)
    DUT.ENABLE.value = 1

    for addr in [base, offset]:
        logger.info(f"Testing address: 0x{addr:08X}")
        for count in range(addr, addr + num_cols, 1):
            await RisingEdge(DUT.CLK)
            check = int(DUT.ADDRESS.value)
            assert count == check, f"Fail current DUT address value {check}. Expected value {count}"
        logger.info("Test Passed.")

    await RisingEdge(DUT.CLK)
    DUT.ENABLE.value = 0
    
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return

