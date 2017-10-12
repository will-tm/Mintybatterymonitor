#!/usr/bin/env python2.7

'''
Date:  10/08/17
Author:  HoolyHoo
Version:  2.0
Name:  Combo Shortcut Script - Utility for the MintyPi project.
Description:  Monitors GPIO interrupts to adjust volume with icons, lcd dimming, battery monitor, wifi and bluetooth toggle, and performs safe shutdown.
Usage:  Mode + Y = Toggle Wifi with Icon
        Mode + B = Toggle BT with Icon
        Mode + A = Toggle Battery
        Mode + X = Initiate Safe Shutdown
        Mode + Dpad Right = Volume Up with Icon
        Mode + Dpad Left  = Volume Down with Icon
        Mode + Dpad Up    = Dimming Up
        Mode + Dpad Down  = Dimming Down
        Mode + Right Shoulder = Display Cheat
'''

from gpiozero import Button
from signal import pause
from subprocess import check_call
import wiringpi
import os
import time


def grabPin(file):
    try:
        with open(file, 'r') as f:
            pin = f.read()
    except IOError:
        with open(file, 'w') as f:
            f.write('7')
        pin = '7'
    return int(pin)


pinFile = "/boot/mintypi/pinfile.txt"
functionPin = grabPin(pinFile)
functionBtn = Button(functionPin)
brightnessUpBtn = Button(4)
brightnessDownBtn = Button(5)
volumeUpBtn = Button(22)
volumeDownBtn = Button(14)
shutdownBtn = Button(26)
monitorBtn = Button(21)
wifiBtn = Button(20)
bluetoothBtn = Button(16)
cheatBtn = Button(6)
led = 1
brightness = 1024
volume = 60
wifiStatus = 1
bluetoothStatus = 1
toggleFile = "/home/pi/Mintybatterymonitor/Toggle.txt"
pngviewPath = "/home/pi/Mintybatterymonitor/Pngview/"
iconPath = "/home/pi/Mintybatterymonitor/icons"


# Functions
def brightnessUp():
    global brightness
    if brightnessUpBtn.is_pressed:
        brightness = min(1024, brightness + 100)
        controlBrightness()


def brightnessDown():
    global brightness
    if brightnessDownBtn.is_pressed:
        brightness = max(0, brightness - 100)
        controlBrightness()


def volumeDown():
    global volume
    volume = max(0, volume - 10)
    os.system("amixer sset -q 'PCM' " + str(volume) + "%")
    showVolumeIcon()


def volumeUp():
    global volume
    volume = min(100, volume + 10)
    os.system("amixer sset -q 'PCM' " + str(volume) + "%")
    showVolumeIcon()


def wifiToggle():
    global wifiStatus
    if wifiStatus == 0:
        os.system("sudo rfkill block wifi")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/wifiOff.png &")
        time.sleep(3)
        killPngview()
        wifiStatus = 1
    else:
        os.system("sudo rfkill unblock wifi")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/wifiOn.png &")
        time.sleep(3)
        killPngview()
        wifiStatus = 0


def bluetoothToggle():
    global bluetoothStatus
    if bluetoothStatus == 0:
        os.system("sudo rfkill block bluetooth")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/bluetoothOff.png &")
        time.sleep(3)
        killPngview()
        bluetoothStatus = 1
    else:
        os.system("sudo rfkill unblock bluetooth")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/bluetoothOn.png &")
        time.sleep(3)
        killPngview()
        bluetoothStatus = 0


def shutdown():
    for i in range(0, 3):
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/shutdown.png &")
        time.sleep(1)
        killPngview()
        time.sleep(.5)
    check_call(['sudo', 'poweroff'])


def toggleState():
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


def showVolumeIcon():
    global volume
    killPngview()
    while volumeUpBtn.is_pressed or volumeDownBtn.is_pressed:
        if volumeUpBtn.is_pressed:
            os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/Volume" + str(volume) + ".png &")
            volume = min(100, volume + 10)
            os.system("amixer sset -q 'PCM' " + str(volume) + "%")
            killPngview()
        elif volumeDownBtn.is_pressed:
            os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/Volume" + str(volume) + ".png &")
            volume = max(0, volume - 10)
            os.system("amixer sset -q 'PCM' " + str(volume) + "%")
            killPngview()
    else:
        os.system("amixer sset -q 'PCM' " + str(volume) + "%")
        os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/Volume" + str(volume) + ".png &")
        time.sleep(2)
        killPngview()


def controlBrightness():
    global brightness
    wiringpi.pwmWrite(led, brightness)
    time.sleep(.2)


def showCheat():
    os.system(pngviewPath + "/pngview2 -b 0 -l 999999 " + iconPath + "/cheat.png &")
    time.sleep(5)
    killPngview()


def killPngview():
    os.system("sudo killall -q -15 pngview2")


def initSetup():
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(led, 2)
    wiringpi.pwmWrite(led, brightness)
    os.system("amixer sset -q 'PCM' " + str(volume) + "%")
    os.system("sudo rfkill block wifi")
    os.system("sudo rfkill block bluetooth")


def checkFunction():
    while functionBtn.is_pressed:
        if brightnessUpBtn.is_pressed:
            brightnessUp()
        elif brightnessDownBtn.is_pressed:
            brightnessDown()
        elif volumeUpBtn.is_pressed:
            volumeUp()
        elif volumeDownBtn.is_pressed:
            volumeDown()
        elif shutdownBtn.is_pressed:
            shutdown()
        elif monitorBtn.is_pressed:
            toggleState()
        elif wifiBtn.is_pressed:
            wifiToggle()
        elif bluetoothBtn.is_pressed:
            bluetoothToggle()
        elif cheatBtn.is_pressed:
            showCheat()


# Initial File Setup
try:
    with open(toggleFile, 'r') as f:
        output = f.read()
except IOError:
    with open(toggleFile, 'w') as f:
        f.write('1')
    output = '1'
state = int(output)
initSetup()


# Interrupt
functionBtn.when_pressed = checkFunction
pause()
