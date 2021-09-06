from usbhonk.usb.functions.function import USBFunction

class ACM(USBFunction):
    """ ACM Serial Device """

    def __init__(self, gadget_path, acm_name):
        super().__init__(gadget_path, f"acm.{acm_name}")

    @property
    def port_num(self) -> int:
        """ Get the port number """
        return self.get_int_val("port_num")
