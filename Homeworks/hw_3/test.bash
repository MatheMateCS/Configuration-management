#!/bin/bash

interpreter="python3"
executable="test.py"

if [ $# -gt 0 ]; then
interpreter=$1; fi

$interpreter $executable