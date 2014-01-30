#!/usr/bin/env python

import subprocess
import os
import calendar
import time
import re
import platform

colors = ['#EA644A','#CC3118','#EC9D48','#CC7016','#ECD748','#C9B215','#54EC48','#24BC14','#48C4EC','#1598C3','#DE48EC','#B415C7','#7648EC','#4D18E4']
numcolors = len(colors)

sizes = {}
totime = calendar.timegm(time.gmtime())
fromtime = totime - 86400
width=800
height=800
hostname=platform.node()

def graph_rrd(filename,label):
    outputfilename = 'images/'+hostname+"/"+label+'.png'
    output = ['rrdtool','graph',outputfilename,'-v Write <-- blocks --> Read','--title',label,'-w',str(width),'-h',str(height),'--start', str(fromtime), '--end', str(totime)]
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

if not os.path.isdir("images/"+hostname):
    os.makedirs("images/"+hostname)

matches = {}
with open('matches.map','r') as file:
    for line in file:
        items = line.split(',')
        matches[re.compile(items[0])] = items[1].rstrip()

maps = {}
with open('maps.map','r') as file:
    for line in file:
        items = line.split(',')
        maps[items[0].upper()] = items[1].rstrip()

for file in os.listdir("rrds/"):
    if file.endswith(".rrd"):
        for item in matches.keys():
            m = item.match(file)
            if m:
                label = matches[item]+m.group(1)
                label=label.upper()
                if label in maps:
                    label = maps[label]
                label = label.replace('/','_')
                print label
                filename = 'rrds/'+file.replace(':','\:')
                graph_rrd(filename,label)


