#!/usr/bin/env python

import subprocess

cmd = subprocess.Popen('zpool status', shell=True, stdout=subprocess.PIPE)

for l in cmd.stdout:
        line = l.split()
        if len(line) > 0 and line[0] == 'NAME':
                p = cmd.stdout.next().split()
                pool = p[0]
                d = cmd.stdout.next().split()
                disk = d[0]
                if 'emcpower' in disk:
                        disk = disk.rstrip('g')
                if 'c5t' in disk:
                        disk = disk.strip('c5t')
                        disk = disk.rstrip('d0')
                print "%s,%s"%(disk,pool)
        

cmd = subprocess.Popen('mount | grep /dev/dsk', shell=True, stdout=subprocess.PIPE)

for l in cmd.stdout:
        line = l.split()
        mount = line[0]
        disk = line[2]
        disk = disk.split('/')[-1]
        disk = disk.rstrip('g')
        print "%s,%s"%(disk,mount)

