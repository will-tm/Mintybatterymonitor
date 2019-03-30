# Mintybatterymonitor!
This script is used in conjuction with Helder's battery monitoring board for the MintyPi.
This script will display a battery icon according to battery level and will show a warning video when reaching low level.  Upon critical battery level, the script will show a critical battery level warning video and then introduce a safe shutdown.  The battery monitoring can be toggled on or off by holding the select button for two seconds.

Also included in this script is an on demand shutdown button script.  If desired, a simple tact switch can be installed to GPIO 7.  The script will monitor that GPIO in the background and invoke a safe shutdown when pressed.

More information can be obtained from this thread:
http://www.sudomod.com/forum/viewtopic.php?f=38&t=3699


#### Automated Software Install

Go to raspberry command prompt or SSH.
Make sure you are in the home directory by typing ```cd ~ ``` and then type:
```
wget https://raw.githubusercontent.com/Will-tm/Mintybatterymonitor/master/MintyInstall.sh
```
Then type:
```
sudo git clone https://github.com/Will-tm/Mintybatterymonitor.git
```
Then type:
```
sudo chmod 777 MintyInstall.sh
```
And then type:
```
sudo ./MintyInstall.sh
```
Finally reboot to have it all start on boot with:
```
sudo reboot
```
