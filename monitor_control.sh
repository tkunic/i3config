#!/bin/bash

usage(){
    echo "USAGE: $0 [VGA/DP] [left/right/above/below/same/off]"
    exit 1
}

if [ $# -lt 2 ]
then
    usage
fi

if [ $1 = "VGA" ]
then
    OUT="DP2"
elif [ $1 = "DP" ]
then
    OUT="HDMI1"
else
    usage
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
else
    usage
fi

xrandr --output $OUT $ACTION
