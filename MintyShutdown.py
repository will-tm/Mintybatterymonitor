from gpiozero import Button
from subprocess import check_call
from signal import pause
import os
import time


toggleFile = '/home/pi/Mintybatterymonitor/Toggle.txt'

try:
    with open(toggleFile, 'r') as f:
        output = f.read()
except IOError:
    with open(toggleFile, 'w') as f:
        f.write('1')
    output = '1'
state = int(output)


def shutdown():
    check_call(['sudo', 'poweroff'])


def togglestate():
    global state
    if state == 1:
        os.system('sudo pkill -f "python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py"')
        state = 0
        with open(toggleFile, 'w') as f:
            f.write('0')
        time.sleep(2)
        os.system("python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py &")
        time.sleep(1)
    else:
        os.system('sudo pkill -f "python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py"')
        state = 1
        with open(toggleFile, 'w') as f:
            f.write('1')
        time.sleep(2)
        os.system("python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py &")
        time.sleep(1)


# Interrupts

shutdown_btn = Button(7, hold_time=1)
monitor_btn = Button(19, hold_time=2)
shutdown_btn.when_held = shutdown
monitor_btn.when_held = togglestate
pause()
