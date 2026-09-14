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

logger = logging.getLogger("address_logic_tb")
logger.setLevel(logging.INFO)
logger.propagate = True


@cocotb.test()
async def logic_test(DUT : HierarchyObject) -> None:
    DUT.RST.value = 1
    DUT.INPUT_CHANGE.value = 0
    DUT.OUTPUT_CHANGE.value = 0
    DUT.DATA_VALID.value = 0
    DUT.DATA_READY.value = 0

    await setup_clock(DUT.CLK, 320e6)
    await Timer(1, unit = "us")

    DUT.RST.value = 0
    await Timer(2, unit = "us")
    await RisingEdge(DUT.CLK)
    DUT.OUTPUT_CHANGE.value = 1
    await RisingEdge(DUT.CLK)
    DUT.OUTPUT_CHANGE.value = 0
    await Timer(1, unit = "us")
    await RisingEdge(DUT.CLK)
    DUT.INPUT_CHANGE.value = 1
    await RisingEdge(DUT.CLK)
    DUT.INPUT_CHANGE.value = 0

    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return