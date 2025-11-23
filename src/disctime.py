#!/usr/bin/env python

import os
import re
import sys
import math
import json


class MapDoorText:
    def __init__(self):
        self.return_value = []
        self.custom_matches = []

    def parse_mdt(self, mdt_line):
        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[error] No input provided.')
        sys.exit()

    argument, mdt_line = sys.argv.pop(1), None

    # Is this a file passed to us?
    if os.path.exists(argument):
        with open(argument, 'r') as f:
            mdt_line = f.readline()

    else:
        mdt_line = argument

    mdt = MapDoorText()
    mdt.parse_mdt(mdt_line)

    for line in mdt.return_value:
        print(line)
