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

logger = logging.getLogger("input_column_counter_tb")
logger.setLevel(logging.INFO)
logger.propagate = True


class counter(object):
    def __init__(self : "counter", init : int = 0) -> None:
        self.count = init

    def increment(self : "counter", incr : int = 1) -> None:
        self.count += incr

    def get_count(self : "counter") -> int:
        return self.count

    def reset(self : "counter", init : int = 0) -> None:
        self.count = init


async def enable_random_pulse(clk : SimHandleBase,
                              signal : SimHandleBase,
                              min_width : int = 5,
                              max_width : int = 150,
                              min_idle : int = 20,
                              max_idle : int = 40) -> None:
    while True:
        idle_cycles = random.randint(min_idle, max_idle)
        await ClockCycles(clk, idle_cycles)
        width_cycles = random.randint(min_width, max_width)
        signal.value = 1
        await ClockCycles(clk, width_cycles)
        signal.value = 0

async def sync_counter(clk : SimHandleBase,
                       rst : SimHandleBase,
                       enable : SimHandleBase,
                       count : counter) -> None:
    while True:
        en_prev = int(enable.value)
        rst_prev = int(rst.value)
        await RisingEdge(clk)
        if (rst_prev == 1):
            count.reset()
        else:
            if (en_prev == 1):
                count.increment()
        logger.debug(f"Tick Tock {count.count}")



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

@cocotb.test()
async def pulsed_enable(DUT : HierarchyObject) -> None:
    logger.info(f"{'*'*33} Starting pulsed enable test {'*'*34}")
    DUT.RST.value = 1
    DUT.ENABLE.value = 0

    logger.info("Creating virtual counter object.")
    COUNTER = counter(-1)
    logger.debug(f"Starting counter integer: {COUNTER.get_count()}")

    num_cycles = 2048
    logger.info(f"Number of cycles to run: {num_cycles}")

    num_cols = int(DUT.C_NUM_COLS.value)
    base = int(DUT.C_BASE_ADDRESS.value)
    offset = int(DUT.C_OFFSET_ADDRESS.value)
    logger.info(f"Testing Number of columns: {num_cols}")
    logger.info(f"Base Address: 0x{base:08X}")
    logger.info(f"offset Address: 0x{offset:08X}")

    logger.info("Starting clock at 325 MHz")
    await setup_clock(DUT.CLK, 200e6)

    logger.info("Detaching random pulse function")
    cocotb.start_soon(sync_counter(DUT.CLK, DUT.RST, DUT.ENABLE, COUNTER))
    cocotb.start_soon(enable_random_pulse(DUT.CLK, DUT.ENABLE))
    await Timer(1, unit = "us")

    logger.info("Deasserting reset")
    DUT.RST.value = 0
    while num_cycles > 0:
        await RisingEdge(DUT.CLK)
        assert DUT.ADDRESS.value == COUNTER.get_count(), (f"Failed DUT Count : " +
            f"{int(DUT.ADDRESS.value)} COUNTER : {COUNTER.get_count()}")
        num_cycles -= 1
    logger.info("Ending test now")
    await Timer(1, "us")
    return