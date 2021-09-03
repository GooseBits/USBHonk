#!/bin/bash -e

echo "Cleaning up..."

apt-get --purge -y autoremove
apt-get -y clean

