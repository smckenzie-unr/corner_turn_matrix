#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
# Suppress DeprecationWarnings specifically stemming from cocotbext
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cocotbext")

import logging
import cocotb
import random
import numpy as np
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles
from cocotb.handle import HierarchyObject, SimHandleBase
from cocotb.types import LogicArray
from cocotbext.axi import AxiStreamBus, AxiStreamSource, AxiStreamSink

from scripts.tb_utils import setup_clock

logger = logging.getLogger("axis_corner_turn_tb")
logger.setLevel(logging.INFO)
logger.propagate = True

@cocotb.test()
async def axis_corner_turn_matrix_test(DUT: HierarchyObject) -> None:
    DUT.AXIS_ARSTN.value = 0
    DUT.S_AXIS_TVALID.value = 0
    DUT.S_AXIS_TDATA.value = 0
    DUT.M_AXIS_TREADY.value = 0

    await setup_clock(DUT.AXIS_ACLK, 320e6)

    axis_source = AxiStreamSource(
        AxiStreamBus.from_prefix(DUT, "S_AXIS"), 
        DUT.AXIS_ACLK, 
        DUT.AXIS_ARSTN
    )
    
    axis_sink = AxiStreamSink(
        AxiStreamBus.from_prefix(DUT, "M_AXIS"), 
        DUT.AXIS_ACLK, 
        DUT.AXIS_ARSTN
    )    

    await Timer(1, unit = "us")
    DUT.AXIS_ARSTN.value = 1
    await Timer(5, unit = "us")
    logger.info("Finished sim")
    await Timer(5, unit = "us")
    return