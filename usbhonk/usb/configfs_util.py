
class ConfigFSWrapper:
    """ Helper utilities for accessing configfs files """

    def __init__(self, path):
        self.path = path

    def get_bool_val(self, name : str) -> bool:
        return self.get_str_val(name) == "1"

    def set_bool_val(self, name : str, value : bool):
        if value:
            self.set_str_val(name, "1")
        else:
            self.set_str_val(name, "0")

    def get_int_val(self, name : str) -> int:
        return int(self.get_str_val(name))

    def set_int_val(self, name : str, value : int):
        self.set_str_val(name, str(value))

    def get_str_val(self, name : str) -> str:
        p = self.path / name
        return p.open().readline().strip()

    def set_str_val(self, name : str, value : bool):
        p = self.path / name
        with p.open() as f:
            f.write(value)
