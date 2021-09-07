#!/bin/bash -e

###
### Install USBHonk
###

VENV="/opt/usbhonk"

# Install dependencies
# python3-pip and python3-venv needed for our virtual environment
# cryptsetup needed for LUKS stuff
#
# python3-dbus and python3-gi are needed for our bluetooth agent.
# 
apt-get install -y python3-pip python3-venv python3-pydbus python3-gi cryptsetup
# libglib2.0-dev libgirepository1.0-dev libcairo2-dev

# Create the venv and activate it.
# --system-site-packages is used because pydbus needs
# several dev packages and has to be compiled. Easier
# to just allow the system packages in.
python3 -m venv --system-site-packages "$VENV"
. ${VENV}/bin/activate

# Install the wheel
python3 -m pip install /tmp/chroot_installer/usbhonk*.whl

# Add a wrapper script for the usbhonk shell
cat << EOF > ${VENV}/bin/shell.sh
#!/bin/bash

##
## Wrapper script for the goose user's shell
##
/usr/bin/sudo ${VENV}/bin/python3 -m usbhonk
EOF
chmod +x "${VENV}/bin/shell.sh"

# Adjust the shell for the goose user
usermod --shell "${VENV}/bin/shell.sh" "$GOOSE_USER"

# Startup script
cat << 'EOF' > /lib/systemd/system/usbhonk_gadget.service
[Unit]
Description=USBHonk default gadget
Before=serial-getty@ttyGS0.service

[Service]
Type=oneshot
ExecStart=/opt/usbhonk/bin/python3 -m usbhonk.usb.gadgets.default_gadget --activate
ExecStop=/opt/usbhonk/bin/python3 -m usbhonk.usb.gadgets.default_gadget --deactivate
RemainAfterExit=true

[Install]
WantedBy=basic.target
EOF

/usr/bin/systemctl enable usbhonk_gadget.service
/usr/bin/systemctl enable serial-getty@ttyGS0.service