#!/bin/bash -e

cat << 'EOF' >> /etc/modules.conf
# Act as a composite USB device
libcomposite

# Make sure this is the first loaded function, 
# Windows needs it to be slot 0 in a composite device
usb_f_rndis
EOF