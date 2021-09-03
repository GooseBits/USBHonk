#!/bin/bash -e

echo "Configuring a read-only rootfs..."

# Remove some packages
apt-get -y remove --purge triggerhappy logrotate dphys-swapfile

# Remove some startup scripts and timers
systemctl disable bootlogs
systemctl disable console-setup

systemctl disable apt-daily.timer
systemctl disable apt-daily-upgrade.timer
systemctl disable man-db.timer

# Replace rsyslog with busybox-syslogd
apt-get install -y busybox-syslogd
dpkg --purge rsyslog

# Add tmpfs entries to fstab
cat << EOF >> /etc/fstab

# tmpfs for directories that need r/w
tmpfs           /var/lib/dhcp           tmpfs   defaults,nosuid,nodev         0       0
tmpfs           /var/lib/dhcpcd5        tmpfs   defaults,nosuid,nodev         0       0
tmpfs           /run                    tmpfs   defaults,nosuid,nodev         0       0
tmpfs           /tmp                    tmpfs   defaults,nosuid,nodev         0       0
tmpfs           /var/log                tmpfs   defaults,nosuid,nodev         0       0
tmpfs           /var/spool              tmpfs   defaults,nosuid,nodev         0       0
EOF

# Move the random seed to /tmp
sed -i 's~^ExecStart=~ExecStartPre=/bin/echo "" >/tmp/random-seed\nExecStart=~' /lib/systemd/system/systemd-random-seed.service
rm -f /var/lib/systemd/random-seed
ln -s /tmp/random-seed /var/lib/systemd/random-seed
systemctl daemon-reload

# Change /boot/cmdline.txt for read only boot
sed -i 's~$~ fastboot noswap ro~' /boot/cmdline.txt
