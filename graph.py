#!/usr/bin/env python

import subprocess
import os

sizes = {}

def graph_rrd(filename):
    output = ['rrdtool','graph','dan.png','--start', '1390776000', '--end', '1390850042']
    for i in range(8,22):
        bin_ = 2**i
        o = "DEF:"+str(bin_)+'='+filename+':'+str(bin_)+':AVERAGE'
        output.append(o)
        o = "LINE2:"+str(bin_)+'#FF0000'
        output.append(o)
    subprocess.check_output(output)

graph_rrd('rrds/iosize-??.rrd')

