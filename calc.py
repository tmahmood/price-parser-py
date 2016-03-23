#!/usr/bin/env python
# encoding: utf-8

import sys

PER_POUND = 135
CHARGE_PER_KG = 600

if len(sys.argv) < 2:
    print("missing url to parse")
    sys.exit(1)
price = int(sys.argv[1])
weight = int(sys.argv[2])

print((PER_POUND * price) + ((weight / 1000) * CHARGE_PER_KG))
