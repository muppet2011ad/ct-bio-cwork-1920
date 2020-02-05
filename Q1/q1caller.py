# Simple test script to make it easier to run tests

import sys, os

length = sys.argv[1]

os.system("python jsbl33_q1.py TestFiles/length" + length + "_A.txt TestFiles/length" + length + "_B.txt")