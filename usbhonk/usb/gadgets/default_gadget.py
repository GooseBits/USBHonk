#!/usr/bin/env python3

import argparse

from usbhonk.usb.gadget import USBGadget
from usbhonk.usb.functions.acm import ACM
from usbhonk.usb.functions.mass_storage import MassStorage,LUN
from usbhonk.usb.functions.rndis import RNDIS

class DefaultGadget(USBGadget):
    """ The default gadget for USBHonk """
    def __init__(self):
        USBGadget.__init__(self, "default_gadget")

        ## Configure settings
        self.bcdDevice = 0x0100 # v1.0.0
        self.bcdUSB = 0x0200    # USB 2.0
        self.idVendor = 0x1d6b  # Linux Foundation
        self.idProduct = 0x7104 # Some randomly chosen value

        # Special values to make Windows happy
        self.bDeviceClass = 0xEF
        self.bDeviceSubClass = 0x02
        self.bDeviceProtocol = 0x01

        # Gadget Strings
        # TODO
        #mkdir -p strings/0x409
        #echo "deadbeef00115599" > strings/0x409/serialnumber
        #echo "GooseBits"        > strings/0x409/manufacturer
        #echo "USBHonk"   > strings/0x409/product

        ## Add some functions

        # Networking
        # TODO: This should be configurable to be ecm instead
        self.rndis = self.function(RNDIS, "usb0")

        # Mass storage
        self.mass_storage = self.function(MassStorage, "usb0")

        self.lun0 = self.mass_storage.lun(0)
        self.lun1 = self.mass_storage.lun(1)

        # ACM Serial
        self.acm = self.function(ACM, "usb0")

        # Create the configuration and link in the functions
        self.config = self.configuration("c.1")
        self.config.link_function(self.rndis)
        self.config.link_function(self.mass_storage)
        self.config.link_function(self.acm)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Configure the default usbhonk gadget')
    parser.add_argument('--activate', action='store_true', help="Activate the gadget")
    parser.add_argument('--deactivate', action='store_true', help="Deactivate the gadget")

    args = parser.parse_args()

    g = DefaultGadget()
    if args.activate:
        g.active = True
    if args.deactivate:
        g.active = False