#!/bin/bash

arg0="main.py"
arg1="~/Mermaid/mermaid"
arg2="test_repo"
arg3="graph.mermaid"
arg4="master"

if [ $# -gt 0 ]; then
arg1=$1; fi

if [ $# -gt 1 ]; then
arg2=$2; fi

if [ $# -gt 2 ]; then
arg3=$3; fi

if [ $# -gt 3 ]; then
arg4=$4; fi

python3 $arg0 $arg1 $arg2 $arg3 $arg4