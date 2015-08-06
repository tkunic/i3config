#!/bin/bash

export DISPLAY=:0

LOW_PERCENTAGE=15
VERY_LOW_PERCENTAGE=5

battery_percentage=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage | awk '{print $NF'} | tr -d '%'`
battery_status=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep state | awk '{print $NF'}`

if [ $battery_percentage -lt $LOW_PERCENTAGE ] && [ $battery_status = 'discharging' ]
then
    i3-nagbar -m "Battery is at $battery_percentage%!" -b 'Suspend' 'systemctl suspend'
    if [ $battery_percentage -lt $VERY_LOW_PERCENTAGE ]
    then
        # The battery too low, to prevent violent poweroff, suspend computer.
        systemctl suspend
    fi
fi
