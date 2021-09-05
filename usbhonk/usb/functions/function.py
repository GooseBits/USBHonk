from pathlib import Path

class USBFunction:
    """ Represents a function in a USB gadget """
    def __init__(self, gadget_path, function_name):
        self.path = gadget_path / "functions" / function_name



