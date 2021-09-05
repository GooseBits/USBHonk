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
