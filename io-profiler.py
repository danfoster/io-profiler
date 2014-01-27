#!/usr/bin/env python

import subprocess
import os

sizes = {}

def create_rrd(filename):
    output = ['rrdtool','create',filename]
    for i in range(8,22):
        bin_ = 2**i
        o = "DS:"+str(bin_)+':GAUGE:600:U:U'
        output.append(o)
    output.append('RRA:AVERAGE:0.5:1:24')
    output.append('RRA:AVERAGE:0.5:6:48')
    subprocess.Popen(' '.join(output),shell=True, stdout=subprocess.PIPE)

while True:
    cmd = subprocess.Popen('./io-profiler.d', shell=True, stdout=subprocess.PIPE)
    for line in cmd.stdout:
        disk = ""
        # Get Disk Name
        for line in cmd.stdout:
            l = line.strip()
            if len(l) > 0:
                disk = l
                break

        if disk != "":
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
            filename = 'rrds/iosize-'+disk+'.rrd'

            if not os.path.isfile(filename):
                create_rrd(filename)
            c = ['rrdtool','update',filename,'--template',keys, values]
            output = subprocess.Popen(' '.join(c),shell=True, stdout=subprocess.PIPE)

