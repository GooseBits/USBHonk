#!/bin/bash -e

##
## Change the hostname
##

HOSTNAME="USBHonk"

echo "$HOSTNAME" > /etc/hostname
sed -i "s/raspberrypi/$HOSTNAME/g" /etc/hosts
