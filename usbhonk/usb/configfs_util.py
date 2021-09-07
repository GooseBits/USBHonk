
class ConfigFSWrapper:
    """ Helper utilities for accessing configfs files """

    def __init__(self, path):
        self.path = path

    def get_bool_val(self, name: str) -> bool:
        return self.get_str_val(name) == "1"

    def set_bool_val(self, name: str, value: bool) -> None:
        if value:
            self.set_str_val(name, "1")
        else:
            self.set_str_val(name, "0")

    def get_int_val(self, name: str) -> int:
        return int(self.get_str_val(name), 0)

    def set_int_val(self, name: str, value: int) -> None:
        self.set_str_val(name, str(value))

    def get_str_val(self, name: str) -> str:
        p = self.path / name
        return p.read_text().strip(" \n\t\x00")

    def set_str_val(self, name: str, value: str) -> None:
        p = self.path / name
        if value:
            p.write_text(value)
        else:
            # Nothing happens if the string is completely empty
            # Adding a newline fixes it
            p.write_text("\n")

    def get_bin_val(self, name: str) -> bytes:
        p = self.path / name
        return p.read_bytes()

    def set_bin_val(self, name: str, value: bytes) -> None:
        p = self.path / name
        p.write_bytes(value)
