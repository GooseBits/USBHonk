#!/bin/bash -e

##
## Setup Bluetooth connectivity
## 

##
## Install packages
##
apt-get install -y bluez-tools

##
## systemd Network configuration for pan0
##
mkdir -p /etc/systemd/network
cat << 'EOF' > /etc/systemd/network/pan0.netdev
[NetDev]
Name=pan0
Kind=bridge
EOF

cat << 'EOF' > /etc/systemd/network/pan0.network
[Match]
Name=pan0

[Network]
Address=10.42.0.1/24
DHCPServer=yes
IPv6SendRA=no

[DHCPServer]
# Enable to act as a gateway
EmitDNS=no
EmitRouter=no
DNS=10.42.0.1
EOF

##
## Startup script for bluetooth networking
##
cat << 'EOF' > /lib/systemd/system/bt-network.service
[Unit]
Description=Bluetooth NEP PAN
After=bluetooth.service
Requires=bluetooth.service

[Service]
ExecStart=/usr/bin/bt-network -s nap pan0
Type=simple

[Install]
WantedBy=bluetooth.target
EOF

/usr/bin/systemctl enable bt-network
/usr/bin/systemctl enable systemd-networkd