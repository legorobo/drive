#!/bin/bash
source /etc/bash_completion.d/virtualenvwrapper
workon ev3_py34
echo Started virtualenv
python Drive_Main.py
sleep 5
