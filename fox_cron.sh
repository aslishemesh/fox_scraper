#!/bin/bash
# A simple script

echo -e “Running nosetests…”
./venv/bin/nosetests -s >> asli.log
./venv/bin/python fox_runner.py
echo “Finished !”
