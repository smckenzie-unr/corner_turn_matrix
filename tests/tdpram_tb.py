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
async def tdpram_simulation(DUT : HierarchyObject) -> None:
    await setup_clock(DUT.CLK_A, 200e6)
    await Timer(1, unit = "us")

    # logger.info("Starting test. Filling port B with down count")
    # DUT.WRITE_EN_A.value = 3
    # for i in range(0, 1024, 1):
    #     await RisingEdge(DUT.CLK_A)
    #     DUT.ADDRESS_A.value = i
    #     DUT.DATA_IN_A.value = 1023 - i
    # DUT.WRITE_EN_A.value = 0

    # logger.info("Reading back from port B")
    # DUT.ENABLE_B.value = 1
    # for i in range(0, 1024, 1):
    #     await RisingEdge(DUT.CLK_A)
    #     DUT.ADDRESS_B.value = i
    #     # if (i > 0):
    #     #     assert int(DUT.DATA_OUT_B.value) == (1025 - i), "Memory read back error."
    # DUT.ENABLE_B.value = 0

    # Write phase
    DUT.WRITE_EN_A.value = 3
    for i in range(1024):
        DUT.ADDRESS_A.value = i
        DUT.DATA_IN_A.value = 1023 - i
        await RisingEdge(DUT.CLK_A)
    DUT.WRITE_EN_A.value = 0

    # Read phase
    logger.info("Reading back from port B")
    DUT.ENABLE_B.value = 1

    # Pipeline prime
    await RisingEdge(DUT.CLK_A)

    for i in range(1024):
        DUT.ADDRESS_B.value = i
        await RisingEdge(DUT.CLK_A)  # required latency
        # assert int(DUT.DATA_OUT_B.value) == (1023 - i)

    DUT.ENABLE_B.value = 0

    
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return