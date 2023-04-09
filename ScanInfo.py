#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

pat_in = re.compile( r'(.+): +(.+)' )

# read configuration file for setting webdriver
def ReadInfo(path_in):
    scan_info = {}
    with open(path_in, 'r') as f:
        for lin in f:
            lin = lin.strip()
            if not lin or re.match( r'#', lin ):
                continue
            res = pat_in.fullmatch(lin)
            if res:
                scan_info[res.group(1)] = res.group(2)
    return scan_info
