#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import cocotb
import numpy as np
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.handle import HierarchyObject, SimHandleBase

logger = logging.getLogger("input_column_counter_tb")
logger.setLevel(logging.DEBUG)
logger.propagate = True

async def setup_clock(signal : SimHandleBase, freq : float, df : float = 0.5) -> None:
    T = int(1 / freq * 1e12)
    T_high = int(np.ceil(T * df))
    logger.debug(f"Period: {T}. Period High: {T_high}")
    clk = Clock(signal, period = T, period_high = T_high, unit = "ps")
    cocotb.start_soon(clk.start())

@cocotb.test()
async def constant_enable(DUT : HierarchyObject) -> None:
    DUT.RST.value = 1
    DUT.ENABLE.value = 0
    DUT.OFFSET.value = 0

    await setup_clock(DUT.CLK, 325e6)

    await Timer(1, unit = "us")
    DUT.RST.value = 0
    await Timer(1, unit = "us")

    DUT.ENABLE.value = 1

    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return

