#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
filepath = sys.argv[1]

cpu.load(filepath)
cpu.run()