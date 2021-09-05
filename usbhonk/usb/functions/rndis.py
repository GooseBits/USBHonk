from usbhonk.usb.functions.function import USBFunction

class RNDIS(USBFunction):
    """ Network adapter supported by Windows """

    def __init__(self, gadget_path, rndis_name):
        super().__init__(gadget_path, f"rndis.{rndis_name}")

    @property
    def device_class(self) -> int:
        """ Get the device class """
        return self.get_int_val("class")

    @device_class.setter
    def device_class(self, value : int):
        """ Set the device class """
        return self.set_int_val("class", value)

    @property
    def dev_addr(self) -> str:
        """ Get the device MAC address """
        return self.get_str_val("dev_addr")

    @dev_addr.setter
    def dev_addr(self, addr):
        """ Set the device MAC address """
        self.set_str_val("dev_addr", addr)

    @property
    def host_addr(self) -> str:
        """ Get the host MAC address """
        return self.get_str_val("host_addr")

    @host_addr.setter
    def host_addr(self, addr) :
        """ Set the host MAC address """
        self.set_str_val("host_addr", addr)

    @property
    def ifname(self) -> int:
        """ Get the device interface name """
        return self.get_str_val("ifname")

    @property
    def protocol(self) -> int:
        """ Get the device protocol """
        return self.get_int_val("protocol")

    @protocol.setter
    def protocol(self, value : int):
        """ Set the device protocol """
        return self.set_int_val("protocol", value)

    @property
    def qmult(self) -> int:
        """ Get the qmult value (TODO What is this) """
        return self.get_int_val("qmult")

    @qmult.setter
    def qmult(self, value : int):
        """ Set the qmult value (TODO What is this) """
        return self.set_int_val("qmult", value)

    @property
    def device_subclass(self) -> int:
        """ Get the device subclass """
        return self.get_int_val("subclass")

    @device_subclass.setter
    def device_subclass(self, value : int):
        """ Set the device subclass """
        return self.set_int_val("subclass", value)
