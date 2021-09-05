from usbhonk.usb.functions.function import USBFunction
from usbhonk.usb.configfs_util import ConfigFSWrapper

from pathlib import Path

class USBGadget(ConfigFSWrapper):
    """ USB Gadget Base Class """
    def __init__(self, gadget_name):
        ConfigFSWrapper.__init__(self, Path(f"/sys/kernel/config/usb_gadget/{gadget_name}"))
        self.path.mkdir(parents=True)
        self.__functions = []

    def __del__(self):
        self.active = False
        # TODO: Unlink everything

    def add_function(self, func_class : USBFunction, name : str = "usb0") -> USBFunction:
        """ Create a new function """
        func = func_class(self.path, name)
        self.__functions.append(func)
        return func

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

