#!/bin/bash

source ../venv/bin/activate
python ./run.py rfts:$1> out/rfts/o.$1.txt
