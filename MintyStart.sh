#!/usr/bin/env bash

python /home/pi/Mintybatterymonitor/MintyShutdown.py &
sleep 27
python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py &
