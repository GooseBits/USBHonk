from usbhonk.usb.functions.function import USBFunction


class HID(USBFunction):
    """ USB Human Interface Device """

    def __init__(self, gadget_path, hid_name):
        super().__init__(gadget_path, f"hid.{hid_name}")

    @property
    def dev(self) -> str:
        """ Get the device string """
        return self.get_str_val("dev")

    @dev.setter
    def dev(self, value: str) -> None:
        """ Set the device string """
        return self.set_str_val("dev", value)

    @property
    def protocol(self) -> int:
        """ Get the device protocol """
        return self.get_int_val("protocol")

    @protocol.setter
    def protocol(self, value: int) -> None:
        """ Set the device string """
        return self.set_int_val("protocol", value)

    @property
    def report_desc(self) -> bytes:
        """ Get the report descriptor """
        return self.get_bin_val("report_desc")

    @report_desc.setter
    def report_desc(self, value: bytes) -> None:
        """ Set the report descriptor """
        return self.set_bin_val("report_desc", value)

    @property
    def report_length(self) -> int:
        """ Get the report length """
        return self.get_int_val("report_length")

    @report_length.setter
    def report_length(self, value: int) -> None:
        """ Set the report length """
        return self.set_int_val("report_length", value)

    @property
    def subclass(self) -> int:
        """ Get the subclass """
        return self.get_int_val("subclass")

    @subclass.setter
    def subclass(self, value: int) -> None:
        """ Set the subclass """
        return self.set_int_val("subclass", value)
