#!/usr/bin/env python

import subprocess
import os
import calendar
import time
import re

colors = ['#EA644A','#CC3118','#EC9D48','#CC7016','#ECD748','#C9B215','#54EC48','#24BC14','#48C4EC','#1598C3','#DE48EC','#B415C7','#7648EC','#4D18E4']
numcolors = len(colors)

sizes = {}
totime = calendar.timegm(time.gmtime())
fromtime = totime - 86400
width=800
height=800

def graph_rrd(filename,outputfilename):
    output = ['rrdtool','graph',outputfilename,'--title',outputfilename,'-w',str(width),'-h',str(height),'--start', str(fromtime), '--end', str(totime)]
    count = 0
    stack = ""
    for i in range(12,22):
        bin_ = 2**i
        o = "DEF:read-"+str(bin_)+'='+filename+':read-'+str(bin_)+':AVERAGE'
        output.append(o)
        o = "DEF:writetmp-"+str(bin_)+'='+filename+':write-'+str(bin_)+':AVERAGE'
        output.append(o)
        o = "CDEF:write-"+str(bin_)+'=writetmp-'+str(bin_)+',-1,*'
        output.append(o)
        o = "AREA:read-"+str(bin_)+''+colors[count]+":Read "+str(bin_)+" blocks"+stack
        output.append(o)
        o = "AREA:write-"+str(bin_)+colors[count]+":Write"+str(bin_)+" blocks"+stack
        output.append(o)
        count = (count+1)%numcolors
        stack = ":STACK"
    foo = subprocess.check_output(output)

iscsi=re.compile('iosize_devices_scsi_vhci_ssd@g(.*):.*')
powerpath=re.compile('iosize_devices_pseudo_emcp@(.*):.*')

for file in os.listdir("rrds/"):
    if file.endswith(".rrd"):
        m = iscsi.match(file)
        if m:
            filename = 'rrds/'+file.replace(':','\:')
            outputfilename = 'images/'+m.group(1)+'.png'
            graph_rrd(filename,outputfilename)
        m = powerpath.match(file)
        if m:
            filename = 'rrds/'+file.replace(':','\:')
            outputfilename = 'images/powerpath'+m.group(1)+'.png'
            graph_rrd(filename,outputfilename)


