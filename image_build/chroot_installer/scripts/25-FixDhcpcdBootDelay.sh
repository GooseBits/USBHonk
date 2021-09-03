#!/bin/bash -e

###
### Set a timeout for dhcpcd so the system boots faster.
### Otherwise it hangs for a while, waiting for an address.
###
echo "timeout 5" >> /etc/dhcpcd.conf