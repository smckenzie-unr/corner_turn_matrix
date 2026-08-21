#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import cocotb
import random
import numpy as np
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles
from cocotb.handle import HierarchyObject, SimHandleBase
from cocotb.types import LogicArray

from scripts.tb_utils import setup_clock

logger = logging.getLogger("tdpram_tb")
logger.setLevel(logging.INFO)
logger.propagate = True


@cocotb.test()
async def tdpram_distributed_simulation(DUT : HierarchyObject) -> None:
    await setup_clock(DUT.CLK_A, 200e6)
    await Timer(1, unit = "us")

    check_array = np.arange(1023, -1, -1)
    logger.debug(f"Size of check array: {len(check_array)}")

    # Write phase
    await RisingEdge(DUT.CLK_A)
    DUT.WRITE_EN_A.value = 3
    for i in range(0, 1024, 1):
        DUT.ADDRESS_A.value = i
        logger.debug(f"Index: {i}, value: {check_array[i]}")
        DUT.DATA_IN_A.value = int(check_array[i])
        await RisingEdge(DUT.CLK_A)
    DUT.WRITE_EN_A.value = 0

    await Timer(1, unit = "us")

    # Read phase
    logger.info("Reading back from port B")
    await RisingEdge(DUT.CLK_A)
    DUT.ENABLE_B.value = 1

    for i in range(0, 1024, 1):
        DUT.ADDRESS_B.value = i
        await RisingEdge(DUT.CLK_A)
        assert int(DUT.DATA_OUT_B.value) == check_array[i]
    DUT.ENABLE_B.value = 0

    
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return

@cocotb.test()
async def tdpram_bram_simulation(DUT : HierarchyObject) -> None:
    await setup_clock(DUT.CLK_A, 200e6)
    await Timer(1, unit = "us")

    check_array = np.arange(1023, -1, -1)
    logger.debug(f"Size of check array: {len(check_array)}")

    # Write phase
    await RisingEdge(DUT.CLK_A)
    DUT.WRITE_EN_A.value = 3
    for i in range(0, 1024, 1):
        DUT.ADDRESS_A.value = i
        logger.debug(f"Index: {i}, value: {check_array[i]}")
        DUT.DATA_IN_A.value = int(check_array[i])
        await RisingEdge(DUT.CLK_A)
    DUT.WRITE_EN_A.value = 0

    await Timer(1, unit = "us")

    # Read phase
    logger.info("Reading back from port B")
    await RisingEdge(DUT.CLK_A)
    DUT.ENABLE_B.value = 1

    for i in range(0, 1024, 1):
        DUT.ADDRESS_B.value = i
        await RisingEdge(DUT.CLK_A)
        if (i > 0):
            assert int(DUT.DATA_OUT_B.value) == check_array[i - 1]
    DUT.ENABLE_B.value = 0

    
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return