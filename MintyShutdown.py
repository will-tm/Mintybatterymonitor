from gpiozero import Button
from subprocess import check_call
from signal import pause


def shutdown():
    check_call(['sudo', 'poweroff'])


shutdown_btn = Button(7, hold_time=1)
shutdown_btn.when_held = shutdown
pause()
