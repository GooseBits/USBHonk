#!/usr/bin/env python3

import argparse

from usbhonk.usb.gadget import USBGadget
from usbhonk.usb.functions.acm import ACM
from usbhonk.usb.functions.hid import HID
from usbhonk.usb.functions.mass_storage import MassStorage
from usbhonk.usb.functions.rndis import RNDIS


class DefaultGadget(USBGadget):
    """ The default gadget for USBHonk """

    def __init__(self):
        USBGadget.__init__(self, "default_gadget")

        ##
        # Basic device configuration
        ##

        # Configure settings
        self.bcdDevice = 0x0005  # v0.0.5
        self.bcdUSB = 0x0200    # USB 2.0
        self.idVendor = 0x1d6b  # Linux Foundation
        self.idProduct = 0x7104  # Some randomly chosen value

        # Special values to make Windows happy
        self.bDeviceClass = 0xEF
        self.bDeviceSubClass = 0x02
        self.bDeviceProtocol = 0x01

        # Gadget Strings
        # mkdir -p strings/0x409
        self.english_strings = self.strings.english
        self.english_strings.set("serialnumber", "deadbeef00115599")
        self.english_strings.set("manufacturer", "GooseBits")
        self.english_strings.set("product", "USBHonk")

        ##
        # Configure the OS descriptor to make Windows happy
        ##
        os_desc = self.os_desc
        os_desc.b_vendor_code = 0xcd
        os_desc.qw_sign = "MSFT100"
        os_desc.use = True

        ##
        # Add some functions
        ##

        #
        # Networking
        #
        host_addr = "6e:b1:d7:7f:bf:53"
        dev_addr = "c6:a6:cd:44:25:be"

        # TODO: This should be configurable to be ecm instead
        self.rndis = self.function(RNDIS, "usb0")
        rndis_os_desc = self.rndis.os_desc
        rndis_os_desc.compatible_id = "RNDIS"
        rndis_os_desc.sub_compatible_id = "5162001"

        # Done like this because if we try to write after the
        # initial setup, we get an error, even if the value
        # is the same.
        if self.rndis.host_addr != host_addr:
            self.rndis.host_addr = host_addr
        if self.rndis.dev_addr != dev_addr:
            self.rndis.dev_addr = dev_addr

        #
        # Mass storage
        #
        self.mass_storage = self.function(MassStorage, "usb0")

        self.lun0 = self.mass_storage.lun(0)
        self.lun0.read_only = True
        self.lun0.removable = True
        self.lun0.cdrom = False
        self.lun0.inquiry_string = "Utilities"

        self.lun1 = self.mass_storage.lun(1)
        self.lun1.read_only = False
        self.lun1.removable = True
        self.lun1.cdrom = False
        self.lun1.inquiry_string = "Secure Storage"

        #
        # ACM Serial
        #
        self.acm = self.function(ACM, "usb0")

        #
        # HID Keyboard
        #
        self.keyboard = self.function(HID, "g0")
        if self.keyboard.protocol != 1:
            self.keyboard.protocol = 1
        if self.keyboard.subclass != 1:
            self.keyboard.subclass = 1
        if self.keyboard.report_length != 8:
            self.keyboard.report_length = 8
        if not self.keyboard.report_desc:
            self.keyboard.report_desc = \
                b"\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25"\
                b"\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05"\
                b"\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91"\
                b"\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65"\
                b"\x81\x00\xc0"

        ##
        # Create the configuration
        ##
        self.config = self.configuration("c.1")
        self.config.MaxPower = 250
        config_strings = self.config.strings.english
        config_strings.set("configuration", "USBHonk Configuration 1")
        os_desc.link_configuration(self.config)  # Tell Windows to use config #1

        #
        # Link the functions to the configuration
        #
        self.config.link_function(self.rndis)
        self.config.link_function(self.mass_storage)
        self.config.link_function(self.acm)
        self.config.link_function(self.keyboard)


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
