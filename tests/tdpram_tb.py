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

logger = logging.getLogger("tdpram_tb")
logger.setLevel(logging.INFO)
logger.propagate = True


@cocotb.test()
async def tdpram_simulation(DUT : HierarchyObject) -> None:
    await setup_clock(DUT.CLK, 200e6)
    await Timer(1, unit = "us")

    logger.info("Deasserting reset")
    
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return