#!/usr/bin/env python

import subprocess
import os
import calendar
import time

colors = ['#EA644A','#CC3118','#EC9D48','#CC7016','#ECD748','#C9B215','#54EC48','#24BC14','#48C4EC','#1598C3','#DE48EC','#B415C7','#7648EC','#4D18E4']
numcolors = len(colors)

sizes = {}
totime = calendar.timegm(time.gmtime())
fromtime = totime - 86400

def graph_rrd(filename):
    output = ['rrdtool','graph','dan.png','-w 1024','-h 768','--start', str(fromtime), '--end', str(totime)]
    count = 0
    stack = ""
    for i in range(8,22):
        bin_ = 2**i
        o = "DEF:"+str(bin_)+'='+filename+':'+str(bin_)+':AVERAGE'
        output.append(o)
        o = "AREA:"+str(bin_)+colors[count]+stack
        output.append(o)
        o = "LINE1:"+str(bin_)+colors[count]+stack
#        output.append(o)
        count = (count+1)%numcolors
        stack = "::STACK"
    foo = subprocess.check_output(output)
    print("*** "+foo)

graph_rrd('rrds/iosize_devices_pci@2,600000_SUNW,qlc@0_fp@0,0_ssd@w5006016946e00dd5,f\:c.rrd')

