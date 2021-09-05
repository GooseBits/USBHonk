#!/bin/bash -e

cat << EOF >> /boot/config.txt
dtoverlay=dwc2,dr_mode=peripheral
gpu_mem=16
EOF