#!/bin/bash

arg="python3"
arg0="main.py"
arg1="visualizer.py"
arg2="test_repo"
arg3="graph.mermaid"
arg4="master"

if [ $# -gt 0 ]; then
arg=$1; fi

if [ $# -gt 1 ]; then
arg0=$2; fi

if [ $# -gt 2 ]; then
arg1=$3; fi

if [ $# -gt 3 ]; then
arg2=$4; fi

if [ $# -gt 4 ]; then
arg3=$5; fi

if [ $# -gt 5 ]; then
arg4=$6; fi

$arg $arg0 $arg1 $arg2 $arg3 $arg4 $arg