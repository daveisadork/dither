#!/usr/bin/env python
import os.path
import sys
from optparse import OptionParser

program_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, program_dir)

parser = OptionParser()

(options, args) = parser.parse_args(sys.argv[1:])

from dither.player import main; 

try: main(args[0])
except IndexError: main(None)
