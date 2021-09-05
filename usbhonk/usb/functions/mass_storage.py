from .function import USBFunction

from pathlib import Path

class LUN:
    """ An individual LUN as part of a mass storage device"""

    def __init__(self, function_path : Path, id : int):
        self.path = function_path / f"lun.{id}"
        self.path.mkdir(parents=True, exist_ok=True)

    def get_bool_val(self, name : str) -> bool:
        return self.get_str_val(name) == "1"

    def set_bool_val(self, name : str, value : bool):
        p = self.path / name
        if value:
            self.set_str_val(name, "1")
        else:
            self.set_str_val(name, "0")

    def get_str_val(self, name : str) -> str:
        p = self.path / name
        return p.open().readline().strip()

    def set_str_val(self, name : str, value : bool):
        p = self.path / name
        with p.open() as f:
            p.write(value)

    @property
    def cdrom(self) -> bool:
        """ Get whether the gadget appears as a cdrom drive """
        return self.get_bool_val("cdrom")

    @cdrom.setter
    def cdrom(self, value : bool):
        """ Set whether the gadget appears as a cdrom drive """
        self.set_bool_val("cdrom", value)

    @property
    def file(self) -> str:
        """ Get the image or device being served """
        return self.get_str_val("file")

    @file.setter
    def file(self, value : str):
        """ Get the image or device being served """
        self.set_str_val("file", value)

    @property
    def inquiry_string(self) -> str:
        """ Get the inquiry_string of the LUN """
        return self.get_str_val("inquiry_string")

    @inquiry_string.setter
    def inquiry_string(self, value : str):
        """ Set the inquiry_string of the LUN """
        self.set_str_val("inquiry_string", value)

    @property
    def nofua(self) -> bool:
        """ Get whether the FUA flag should be ignored """
        return self.get_bool_val("nofua")

    @nofua.setter
    def nofua(self, value : bool):
        """ Set whether the FUA flag should be ignored """
        self.set_bool_val("nofua", value)

    @property
    def removable(self) -> bool:
        """ Get whether LUN is removable """
        return self.get_bool_val("removable")

    @removable.setter
    def removable(self, value : bool):
        """ Set whether LUN is removable """
        self.set_bool_val("removable", value)

    @property
    def read_only(self) -> bool:
        """ Get whether LUN is read-only """
        return self.get_bool_val("ro")

    @read_only.setter
    def read_only(self, value : bool):
        """ Set whether LUN is read-only """
        self.set_bool_val("ro", value)


class MassStorage(USBFunction):
    """ Emulated mass storage """

    def __init__(self, gadget_path, rndis_name):
        super().__init__(gadget_path, f"mass_storage.{rndis_name}")
        # lun.0 is populated by default
        self.__luns = [LUN(0)]

    def add_lun(self):
        """ Add a new LUN """
        id = len(self.__luns)
        self.__luns.append(LUN(self.path, id))

    def lun(self, idx : int) -> LUN:
        """ Get a LUN """
        return self.__luns[idx]

    @property
    def stall(self) -> bool:
        """ Get whether the gadget is allowed to halt bulk endpoints. See gadget docs. """
        return self.get_bool_val("stall")

    @stall.setter
    def stall(self, value : bool):
        """ Set whether the gadget is allowed to halt bulk endpoints. See gadget docs. """
        self.set_bool_val("stall", value)
