#!/bin/bash

# This is a script to write usbhonk.img to an sd card.

set -e

# Run from the directory of the script
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ $EUID != 0 ]; then
    echo "Please run as root"
    exit 1
fi

DEPENDENCIES=( lsblk dd jq )

HAS_DEPS=1
for i in "${DEPENDENCIES[@]}"
do
    if ! command -v $i &> /dev/null
    then
        echo "You are missing $i, make sure it's installed."
        HAS_DEPS=0
    fi
done

LSBLK_OUTPUT=$(lsblk -J --output-all)
DEV_COUNT=$(echo "$LSBLK_OUTPUT" | jq -r '.blockdevices|length' )

declare -a VALID_DEVICES
declare -a MOUNTED_VALID_DEVICES

for (( i = 0; i < $DEV_COUNT; ++i ))
do
    TYPE=$(echo "$LSBLK_OUTPUT" | jq -r .blockdevices[$i].type)
    if [ "$TYPE" != "disk" ];
    then
        continue
    fi

    REMOVABLE=$(echo "$LSBLK_OUTPUT" | jq -r .blockdevices[$i].rm)
    if [ "$REMOVABLE" != "true" ];
    then
        continue
    fi

    NAME=$(echo "$LSBLK_OUTPUT" | jq -r .blockdevices[$i].name)

    MOUNT=$(echo "$LSBLK_OUTPUT" | jq -r .blockdevices[$i].mountpoint)
    if [ "$MOUNT" != "null" ];
    then
        echo "$NAME looks valid, but ignored because it's mounted at $MOUNT"
        continue
    fi

    # Check children
    CHILD_COUNT=$(echo "$LSBLK_OUTPUT" | jq -r ".blockdevices[$i].children|length" )
    CHILD_MOUNTED=0
    for (( j = 0; j < $CHILD_COUNT; ++j ))
    do
        CHILD_NAME=$(echo "$LSBLK_OUTPUT" | jq -r ".blockdevices[$i].children[$j].name" )
        CHILD_MOUNT=$(echo "$LSBLK_OUTPUT" | jq -r ".blockdevices[$i].children[$j].mountpoint" )
        if [ "$CHILD_MOUNT" != "null" ];
        then            
            CHILD_MOUNTED=1
            continue
        fi
    done

    if [[ $CHILD_MOUNTED -ne 0 ]]
    then
        MOUNTED_VALID_DEVICES+=$(echo "$LSBLK_OUTPUT" | jq .blockdevices[$i])
        continue
    fi

    VALID_DEVICES+=$(echo "$LSBLK_OUTPUT" | jq .blockdevices[$i])
done

if [ ${#MOUNTED_VALID_DEVICES[@]} != 0 ]; 
then
    echo ""
    echo "The following devices were skipped because they are mounted:"
    for dev in "${MOUNTED_VALID_DEVICES[@]}"
    do
        VENDOR=$(echo "$dev" | jq -r .vendor)
        MODEL=$(echo "$dev" | jq -r .model)
        DEV_PATH=$(echo "$dev" | jq -r .path)
        echo "$VENDOR $MODEL - $DEV_PATH"
    done
fi

if [ ${#VALID_DEVICES[@]} == 0 ]; 
then
    echo "No suitable devices were found"
    exit 1
fi

echo "Valid devices: "
for ((i = 0; i < ${#VALID_DEVICES[@]}; ++i));
do
    dev=${VALID_DEVICES[$i]}
    VENDOR=$(echo "$dev" | jq -r .vendor)
    MODEL=$(echo "$dev" | jq -r .model)
    DEV_PATH=$(echo "$dev" | jq -r .path)
    printf "%3s %-25s [$DEV_PATH]\n" "$((i+1)))" "$VENDOR $MODEL"
done
echo " Q) Quit"
echo ""
read -p "Select a device: " devnum

case "$devnum" in
  0 | Q | q)
    echo "Quitting..."
    exit 0
    ;;
esac

DEVICE=${VALID_DEVICES[$((devnum-1))]}
if [[ -z "$DEVICE" ]];
then
    echo "Invalid selection"
    exit 1
fi

DEV_PATH=$(echo "$DEVICE" | jq -r .path)
read -p "Is this the right device path (y/n)? [$DEV_PATH]: " answer

if [ "$answer" == "y" ]; then
    echo "HOOOOOOONK! hope you don't need anything on $DEV_PATH"
    dd if=usbhonk.img of=$DEV_PATH bs=8M
    sync
    exit 0
fi

echo "Next time be more sure."
exit 1
