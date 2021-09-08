#!/bin/bash

# This is a script to write usbhonk.img to an sd card.

set -e

# Run from the directory of the script
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ $EUID != 0 ]; then
    echo "Please run as root"
    exit 1
fi

if [ $# -ne 1 ]; then
    echo "Usage: $0 <MicroSD device path>"
    exit 1
fi

devpath=$1
read -p "Is this the right device path (y/n)? [$devpath]: " answer

if [ "$answer" == "y" ]; then
    echo "HOOOOOOONK! hope you don't need anything on $devpath"
    dd if=usbhonk.img of=$devpath bs=8M
    sync
    exit 0
fi

echo "Next time be more sure."
exit 1
