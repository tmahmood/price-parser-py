#!/usr/bin/env python
# encoding: utf-8

import sys

PER_POUND = 130
CHARGE_PER_KG = 600

if len(sys.argv) < 2:
    print("missing url to parse")
    sys.exit(1)
price = float(sys.argv[1])
weight = float(sys.argv[2])

print((PER_POUND * price) + ((weight / 1000) * CHARGE_PER_KG))
