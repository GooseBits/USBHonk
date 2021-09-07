#!/usr/bin/env python3

import argparse

from usbhonk.usb.gadget import USBGadget
from usbhonk.usb.functions.hid import HID


class RazerAttack(USBGadget):
    """ The default gadget for USBHonk """

    def __init__(self):
        USBGadget.__init__(self, "razer_attack")

        ##
        # Basic device configuration
        ##

        # Configure settings
        self.bcdDevice = 0x0101  # v1.0.1
        self.bcdUSB = 0x0200     # USB 2.0
        self.idVendor = 0x1532   # Razer
        self.idProduct = 0x0084  # Some product

        # Special values to make Windows happy
        self.bDeviceClass = 0xEF
        self.bDeviceSubClass = 0x02
        self.bDeviceProtocol = 0x01

        # Gadget Strings
        # mkdir -p strings/0x409
        self.english_strings = self.strings.english
        self.english_strings.set("serialnumber", "deadbeef00115599")
        self.english_strings.set("manufacturer", "Razer")
        self.english_strings.set("product", "Razer Mouse")

        #
        # HID Devices
        #
        self.hids = []
        for i in range(0, 2):
            hid = self.function(HID, f"g{i}")
            self.hids.append(hid)
            if hid.protocol != 2:
                hid.protocol = 2
            if hid.subclass != 1:
                hid.subclass = 1
            if hid.report_length != 6:
                hid.report_length = 6
            if not hid.report_desc:
                hid.report_desc = b"\x05\x01\x09\x02\xa1\x01\x09\x01\xa1\x00\x85\x01\x05\x09\x19\x01\x29\x03\x15\x00\x25\x01\x95\x03\x75\x01\x81\x02\x95\x01\x75\x05\x81\x03\x05\x01\x09\x30\x09\x31\x15\x81\x25\x7f\x75\x08\x95\x02\x81\x06\x95\x02\x75\x08\x81\x01\xc0\xc0\x05\x01\x09\x02\xa1\x01\x09\x01\xa1\x00\x85\x02\x05\x09\x19\x01\x29\x03\x15\x00\x25\x01\x95\x03\x75\x01\x81\x02\x95\x01\x75\x05\x81\x01\x05\x01\x09\x30\x09\x31\x15\x00\x26\xff\x7f\x95\x02\x75\x10\x81\x02\xc0\xc0"

        ##
        # Create the configuration
        ##
        config = self.configuration("c.1")
        config.MaxPower = 250
        config_strings = config.strings.english
        config_strings.set("configuration", "Razer Mouse Configuration")

        #
        # Link the functions to the configuration
        #
        for hid in self.hids:
            config.link_function(hid)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configure the razer attack gadget')
    parser.add_argument('--activate', action='store_true', help="Activate the gadget")
    parser.add_argument('--deactivate', action='store_true', help="Deactivate the gadget")

    args = parser.parse_args()

    g = RazerAttack()
    if args.activate:
        g.active = True
    if args.deactivate:
        g.active = False
