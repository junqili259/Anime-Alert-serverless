#!/bin/bash

cd ./api

if [ ! -d env ]; then
    python3 -m venv env
    pip3 install -r devrequirements.txt
fi

source env/bin/activate
