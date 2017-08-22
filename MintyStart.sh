#!/usr/bin/env bash

python /home/pi/Mintybatterymonitor/MintyShutdown.py &
sleep 25
python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py &
