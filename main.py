#!/usr/bin/env python3
from mypkg.functions import *

inputFile = open('mypkg/input-fields.txt', 'r')
line = inputFile.readline()

# read line each line of input file
while line:
	handleLine(line)
	line = inputFile.readline()

