#!/usr/bin/env python

import subprocess
import os

RRDTOOL='/usr/local/rrdtool-1.2.19/bin/rrdtool'
sizes = {}

def create_rrd(filename):
    output = [RRDTOOL,'create',filename]
    for i in range(5,22):
        bin_ = 2**i
        o = "DS:"+str(bin_)+':GAUGE:600:U:U'
        output.append(o)
    output.append('RRA:AVERAGE:0.5:1:24')
    output.append('RRA:AVERAGE:0.5:6:48')
    subprocess.Popen(' '.join(output),shell=True, stdout=subprocess.PIPE)

while True:
    cmd = subprocess.Popen('./io-profiler.d', shell=True, stdout=subprocess.PIPE)
    cmd.stdout.next()
    for line in cmd.stdout: 
        disk = line.strip()

        if disk != "":
	    disk = disk.replace('/','_')
            # Read and discard header line
            cmd.stdout.next()

            for line in cmd.stdout:
                l = line.split()
                if len(l) == 3:
                    sizes[l[0]] = l[2]
                else:
                    break
            
            keys = ':'.join(sizes.keys())
            values = 'N:'+':'.join(sizes.values())
            filename = 'rrds/iosize'+disk+'.rrd'

            if not os.path.isfile(filename):
                create_rrd(filename)
            c = [RRDTOOL,'update',filename,'--template',keys, values]
            output = subprocess.Popen(' '.join(c),shell=True, stdout=subprocess.PIPE)

