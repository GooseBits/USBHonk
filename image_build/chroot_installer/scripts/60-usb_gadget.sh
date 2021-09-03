#!/bin/bash -e

cat << EOF > /lib/systemd/system/setupgadget.service
[Unit]
Description=Setup USB gadget mode

[Service]
Type=oneshot
ExecStart=/usr/local/sbin/setupgadget.sh
RemainAfterExit=true

[Install]
WantedBy=basic.target
EOF

cat << 'EOF' > /usr/local/sbin/setupgadget.sh
#!/bin/bash

modprobe libcomposite

GADGET=/sys/kernel/config/usb_gadget/g1
mkdir -p $GADGET
cd $GADGET

echo 0xf055 > idVendor
echo 0xcafe > idProduct
echo "Raspberry Pi" > strings/0x409/manufacturer
echo "Pi Zero" > strings/0x409/product

mkdir configs/c.1
mkdir configs/c.1/strings/0x409
echo "Config 1" > configs/c.1/strings/0x409/configuration                                             
echo 500 > configs/c.1/MaxPower
mkdir functions/acm.usb0
ln -s functions/acm.usb0 configs/c.1

ls /sys/class/udc > UDC

EOF

chmod +x /usr/local/sbin/setupgadget.sh

systemctl enable setupgadget.service
systemctl enable serial-getty@ttyGS0.service