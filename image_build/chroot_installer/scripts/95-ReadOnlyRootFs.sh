#!/bin/bash -e

echo "Configuring a read-only rootfs..."

# Remove some packages
apt-get -y remove --purge triggerhappy dphys-swapfile logrotate

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
cat << 'EOF' >> /etc/fstab

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

# Startup script to boot rw the first time
cat << 'EOF' > /lib/systemd/system/firstboot_rw.service
[Unit]
Description=Mount rootfs rw
# Add first-boot rw services here
Before=firstboot_ro.service
Before=regenerate_ssh_host_keys.service

[Service]
Type=oneshot
ExecStart=/usr/bin/mount -o remount,rw /
ExecStartPost=/bin/systemctl disable firstboot_rw.service
RemainAfterExit=true

[Install]
WantedBy=basic.target
EOF
/bin/systemctl enable firstboot_rw.service

cat << 'EOF' > /lib/systemd/system/firstboot_ro.service
[Unit]
Description=Mount rootfs ro
# Add first-boot rw services here
After=firstboot_rw.service
After=regenerate_ssh_host_keys.service

[Service]
Type=oneshot
ExecStartPre=/bin/systemctl disable firstboot_ro.service
ExecStart=/usr/bin/mount -o remount,ro /
RemainAfterExit=true

[Install]
WantedBy=basic.target
EOF
/bin/systemctl enable firstboot_ro.service