from .function import USBFunction

from pathlib import Path

class LUN:
    """ An individual LUN as part of a mass storage device"""

    def __init__(self, function_path : Path, id : int):
        self.path = function_path / f"lun.{id}"

    

class MassStorage(USBFunction):
    """ Emulated mass storage """

    def __init__(self, gadget_path, rndis_name):
        super().__init__(gadget_path, f"mass_storage.{rndis_name}")
        # lun.0 is populated by default
        self.luns = [LUN(0)]

    def add_lun(id : int):
        pass

    def stall(self) -> bool:
        p = self.path / "stall"
        result = p.open().readline().strip()
        return result == "1"

    def stall(self, val : bool):
        p = self.path / "stall"
        with p.open() as f:
            if val:
                p.write("1")
            else:
                p.write("0")
