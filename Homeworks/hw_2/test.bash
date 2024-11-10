#!/bin/bash

arg1="python3"
arg2="test.py"

if [ $# -gt 0 ]; then
arg1=$1; fi

if [ $# -gt 1 ]; then
arg2=$2; fi

$arg1 $arg2