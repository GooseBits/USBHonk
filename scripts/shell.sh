#!/bin/bash

# Wrapper script for the goose user's shell

cd /opt/usbhonk/
. /opt/usbhonk/venv/bin/activate
python3 -m usbhonk.main