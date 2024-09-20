#!/bin/sh

arg1=$(whoami)
arg2=$(hostname)
arg3="root.tar"
arg4="main.py"

if [ $# -gt 0 ]; then
arg1=$1; fi

if [ $# -gt 1 ]; then
arg2=$2; fi

if [ $# -gt 2 ]; then
arg3=$3; fi

if [ $# -gt 3 ]; then
arg4=$4; fi

python3 main.py $arg1 $arg2 $arg3 $arg4
#echo $arg1 $arg2 $arg3 $arg4
