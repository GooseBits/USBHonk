#!/bin/bash -e

##
## Enable an SSH server
##
systemctl enable ssh

#
# Modified to remount root rw during execution
#
cat << 'EOF' > /lib/systemd/system/regenerate_ssh_host_keys.service
[Unit]
Description=Regenerate SSH host keys
Before=ssh.service
ConditionFileIsExecutable=/usr/bin/ssh-keygen

[Service]
Type=oneshot
ExecStartPre=mount -o remount,rw /
ExecStartPre=-/bin/dd if=/dev/hwrng of=/dev/urandom count=1 bs=4096
ExecStartPre=-/bin/sh -c "/bin/rm -f -v /etc/ssh/ssh_host_*_key*"
ExecStart=/usr/bin/ssh-keygen -A -v
ExecStartPost=/bin/systemctl disable regenerate_ssh_host_keys
ExecStartPost=mount -o remount,ro /

[Install]
WantedBy=multi-user.target
EOF