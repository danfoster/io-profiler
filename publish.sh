#!/bin/bash

./gen_maps.py > maps.map
./graph.py
./index.py
scp -r images/* seis:~/public_html/io-profiler/
ssh seis chmod -R o+r public_html/io-profiler
ssh seis chmod o+x public_html/io-profiler/*
