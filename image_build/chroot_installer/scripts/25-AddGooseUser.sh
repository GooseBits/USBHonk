#!/bin/bash -e

##
## Configure the Goose user
##
GOOSE_USER="goose"
GOOSE_PASSWORD="honk"

useradd --create-home --groups adm,dialout,sudo $GOOSE_USER
echo "$GOOSE_USER:$GOOSE_PASSWORD" | chpasswd

# Disable the login banner
touch /home/$GOOSE_USER/.hushlogin
chown $GOOSE_USER:$GOOSE_USER /home/goose/.hushlogin

# Enable sudo with no password for the user
cat << EOF > /etc/sudoers.d/10_${GOOSE_USER}_nopasswd
$GOOSE_USER ALL=(ALL) NOPASSWD: ALL
EOF