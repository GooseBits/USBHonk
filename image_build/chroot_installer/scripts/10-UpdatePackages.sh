#!/bin/bash -e

echo "Updating image..."
apt-get update
apt-get dist-upgrade -y
