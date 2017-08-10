from gpiozero import Button
from subprocess import check_call
from signal import pause
import os
import time


state = 1


def shutdown():
    check_call(['sudo', 'poweroff'])


def togglestate():
    global state
    if state == 1:
        os.system('sudo pkill -f "python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py"')
        state = 0
        time.sleep(5)

    else:
        os.system("python /home/pi/Mintybatterymonitor/MintyBatteryMonitor.py &")
        state = 1
        time.sleep(5)


shutdown_btn = Button(7, hold_time=1)
monitor_btn = Button(19, hold_time=2)
shutdown_btn.when_held = shutdown
monitor_btn.when_held = togglestate
pause()
