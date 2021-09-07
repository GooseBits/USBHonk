from pathlib import Path
from usbhonk.usb.configfs_util import ConfigFSWrapper


class StringLang(ConfigFSWrapper):
    """ Handler for one particular language """

    def __init__(self, base_path: Path, language_id: int):
        ConfigFSWrapper.__init__(self, base_path / hex(language_id))
        self.path.mkdir(exist_ok=True)

    def get(self, name: str) -> str:
        """ Get a string property """
        return self.get_str_val(name)

    def set(self, name: str, value: str) -> None:
        """ Set a string property """
        self.set_str_val(name, value)


class Strings():
    """ USB strings utilty """

    def __init__(self, base_path: Path):
        self.path = base_path / "strings"

    def get_language(self, language_id: int) -> StringLang:
        return StringLang(self.path, language_id)

    @property
    def english(self) -> StringLang:
        return self.get_language(0x409)
