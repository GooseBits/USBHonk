# Image Builder

This directory contains scripts to create a new USBHonk image file.

# How to?

1. Have a USBHonk hardware device. How do you get one? (TODO: How do they get one?)
1. Change into this directory and run `sudo ./update_pi_image.sh`
    * _NOTE: the script will verify you have the required dependencies and will tell you to install them if you don't_
1. Once that's done, build the image with `sudo ./build_image.sh` (same deal with dependencies)
1. Once that's done, write the image to a MicroSD card with `sudo ./write_image.sh <device_path>`
    * __IMPORTANT: Don't mess up the device path. You will not be warned more than once.__
