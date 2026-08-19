#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

os.environ["LM_LICENSE_FILE"] = "/home/slmckenzie/intelFPGA_lite/LR-275828_License.dat"
os.environ["PATH"] = "/home/slmckenzie/intelFPGA_lite/24.1std/questa_fse/bin:/usr/bin:" + os.environ["PATH"]

VIVADO = "/tools/Xilinx/Vivado/2024.1"

XPM_VHDL = f"{VIVADO}/data/ip/xpm/xpm_VCOMP.vhd"
XPM_SV = [
    f"{VIVADO}/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv",
    f"{VIVADO}/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv",
    f"{VIVADO}/data/ip/xpm/xpm_fifo/hdl/xpm_fifo.sv",
]

LIBDIR = "./questa_libs/xpm"

os.makedirs(LIBDIR, exist_ok=True)

subprocess.run(["vlib", LIBDIR])
subprocess.run(["vmap", "xpm", LIBDIR])

subprocess.run(["vcom", "-2008", "-work", "xpm", XPM_VHDL])

for sv in XPM_SV:
    subprocess.run(["vlog", "-work", "xpm", sv])
