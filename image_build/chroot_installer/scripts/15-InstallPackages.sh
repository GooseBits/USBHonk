#!/bin/bash -e

echo "Installing some packages..."

apt-get install -y python3-pip python3-venv vim tor jq git cryptsetup

# Don't start automatically
systemctl disable tor