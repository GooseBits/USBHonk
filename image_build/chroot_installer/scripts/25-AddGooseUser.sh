#!/bin/bash -e

##
## Configure the Goose user
##
USER="goose"
PASSWORD="honk"

useradd --create-home --groups adm,dialout,sudo --shell /opt/usbhonk/scripts/shell.sh $USER
echo "$USER:$PASSWORD" | chpasswd

# Disable the login banner
touch /home/$USER/.hushlogin
chown $USER:$USER /home/goose/.hushlogin

# Enable sudo with no password for the user
cat << EOF > /etc/sudoers.d/10_${USER}_nopasswd
$USER ALL=(ALL) NOPASSWD: ALL
EOF