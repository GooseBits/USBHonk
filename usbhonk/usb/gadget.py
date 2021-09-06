from usbhonk.usb.functions.function import USBFunction
from usbhonk.usb.configfs_util import ConfigFSWrapper

from pathlib import Path

class GadgetConfiguration(ConfigFSWrapper):
    """ Gadget configuration """
    def __init__(self, gadget_path, name):
        self.path = gadget_path / "configs" / name
        self.path.mkdir(exist_ok=True)

    def link_function(self, function : USBFunction):
        """ Link a function into this configuration """
        target = self.path / function.path.name
        if not target.exists():
            target.symlink_to(function.path)

class USBGadget(ConfigFSWrapper):
    """ USB Gadget Base Class """
    def __init__(self, gadget_name):
        ConfigFSWrapper.__init__(self, Path(f"/sys/kernel/config/usb_gadget/{gadget_name}"))
        self.path.mkdir(parents=True, exist_ok=True)

    def function(self, func_class : USBFunction, name : str = "usb0") -> USBFunction:
        """ Get or create a function """
        return func_class(self.path, name)

    def configuration(self, name : str) -> GadgetConfiguration:
        """ Get or create a configuration """
        return GadgetConfiguration(self.path, name)

    @property
    def bcdDevice(self) -> int:
        return self.get_int_val("bcdDevice")

    @bcdDevice.setter
    def bcdDevice(self, value : int):
        self.set_int_val("bcdDevice", value)

    @property
    def bcdUSB(self) -> int:
        return self.get_int_val("bcdUSB")

    @bcdUSB.setter
    def bcdUSB(self, value : int):
        self.set_int_val("bcdUSB", value)

    @property
    def bDeviceClass(self) -> int:
        return self.get_int_val("bDeviceClass")

    @bDeviceClass.setter
    def bDeviceClass(self, value : int):
        self.set_int_val("bDeviceClass", value)

    @property
    def bDeviceProtocol(self) -> int:
        return self.get_int_val("bDeviceProtocol")

    @bDeviceProtocol.setter
    def bDeviceProtocol(self, value : int):
        self.set_int_val("bDeviceProtocol", value)

    @property
    def bDeviceSubClass(self) -> int:
        return self.get_int_val("bDeviceSubClass")

    @bDeviceSubClass.setter
    def bDeviceSubClass(self, value : int):
        self.set_int_val("bDeviceSubClass", value)

    @property
    def bMaxPacketSize0(self) -> int:
        return self.get_int_val("bMaxPacketSize0")

    @bMaxPacketSize0.setter
    def bMaxPacketSize0(self, value : int):
        self.set_int_val("bMaxPacketSize0", value)

    @property
    def idProduct(self) -> int:
        return self.get_int_val("idProduct")

    @idProduct.setter
    def idProduct(self, value : int):
        self.set_int_val("idProduct", value)        

    @property
    def idVendor(self) -> int:
        return self.get_int_val("idVendor")

    @idVendor.setter
    def idVendor(self, value : int):
        self.set_int_val("idVendor", value)        

    @property
    def max_speed(self) -> str:
        return self.get_int_val("max_speed")

    @max_speed.setter
    def max_speed(self, value : str):
        self.set_str_val("max_speed", value) 

    @property
    def active(self) -> bool:
        """ Returns true if the gadget is currently active """
        return self.get_str_val("UDC") != ""

    @active.setter
    def active(self, value : bool):
        """ Toggle if the gadget is active """
        if self.active == value:
            return

        setting = ""
        if value:
            # TODO: This is specific to the Pi Zero W
            setting = "20980000.usb"

        self.set_str_val("UDC", setting)

