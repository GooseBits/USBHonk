#!/bin/bash -e

###
### Install USBHonk
###

VENV="/opt/usbhonk"

# Install dependencies
apt-get install -y python3-pip python3-venv cryptsetup

# Create the venv and activate it
python3 -m venv "$VENV"
. ${VENV}/bin/activate

# Install the wheel
python3 -m pip install /tmp/chroot_installer/usbhonk*.whl

# Add a wrapper script for the usbhonk shell
cat << EOF > ${VENV}/bin/shell.sh
#!/bin/bash

##
## Wrapper script for the goose user's shell
##
${VENV}/bin/python3 -m usbhonk
EOF
chmod +x "${VENV}/bin/shell.sh"

# Adjust the shell for the goose user
usermod --shell "${VENV}/bin/shell.sh" "$GOOSE_USER"

# Startup script
cat << 'EOF' > /lib/systemd/system/goosehonk.service
[Unit]
Description=Goosehonk default gadget

[Service]
Type=oneshot
# Detach any existing devices
ExecStartPre=/usr/bin/find /sys/kernel/config/usb_gadget/ -name UDC -exec sh -c 'echo "" > {} ' \; 2&>1 > /dev/null|| true
ExecStart=/opt/goosehonk/bin/python3 -m usbhonk.usb.gadgets.default_gadget --activate
ExecStartPost=/usr/bin/systemctl start serial-getty@ttyGS0.service

ExecStop=/usr/bin/systemctl stop serial-getty@ttyGS0.service
ExecStop=/opt/goosehonk/bin/python3 -m usbhonk.usb.gadgets.default_gadget --deactivate
RemainAfterExit=true

[Install]
WantedBy=basic.target
EOF

/usr/bin/systemctl enable goosehonk.service