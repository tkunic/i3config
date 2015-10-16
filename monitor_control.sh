#!/bin/bash

if [ $# -lt 2 ]
then
    echo "USAGE: $0 [VGA/DP] [left/right/above/below/same/off]"
    exit 1
fi

if [ $1 = "VGA" ]
then
    OUT="DP2"
elif [ $1 = "DP" ]
then
    OUT="HDMI1"
else
    echo "ERROR: Unrecognized option $1"
fi

if [ $2 = "left" ]
then
    ACTION="--auto --left-of eDP1"
elif [ $2 = "right" ]
then
    ACTION="--auto --right-of eDP1"
elif [ $2 = "above" ]
then
    ACTION="--auto --above eDP1"
elif [ $2 = "below" ]
then
    ACTION="--auto --below eDP1"
elif [ $2 = "same" ]
then
    ACTION="--auto --same-as eDP1"
elif [ $2 = "off" ]
then
    ACTION="--off"
fi

xrandr --output $OUT $ACTION
