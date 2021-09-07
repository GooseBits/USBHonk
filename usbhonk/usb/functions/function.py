from pathlib import Path
from usbhonk.usb.configfs_util import ConfigFSWrapper


class USBFunction(ConfigFSWrapper):
    """ Represents a function in a USB gadget """

    def __init__(self, gadget_path: Path, function_name: str):
        ConfigFSWrapper.__init__(self, gadget_path / "functions" / function_name)
        self.path.mkdir(parents=True, exist_ok=True)
