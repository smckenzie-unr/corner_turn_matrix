#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from cocotb import start_soon
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from cocotb.handle import HierarchyObject, SimHandleBase

async def setup_clock(signal : SimHandleBase, freq : float, df : float = 0.5) -> None:
    """
    Create and start a cocotb clock on a given signal

    Parameters
    ----------
    signal : SimHandleBase
        The clock signal that will be use to generate a clock oscilation
    freq : float
        The frequency that the synthetic clock should be set to
    df : float
        The duty factor for the synthetic clock signal. Default is 0.5

    Returns
    -------
    None    
    """

    # Get the period of the clock oscillation
    T = int(1 / freq * 1e12)

    # Calculate the time the clock signal is high
    T_high = int(np.ceil(T * df))

    # Generate the cocotb clock signal
    clk = Clock(signal, period = T, period_high = T_high, unit = "ps")

    # Start the clock signal to be free running
    start_soon(clk.start())