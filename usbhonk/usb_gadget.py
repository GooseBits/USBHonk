from pathlib import Path

class USBGadget:
    """ USB Gadget Base Class """
    def __init__(self, name):
        self.path = Path(f"/sys/kernel/config/usb_gadget/{name}")
        self.path.mkdir(parents=True)

    def __del__(self):
        if self.is_active():
            self.deactivate()
        # TODO: Unlink

    def is_active() -> bool:
        pass

    def activate():
        pass

    def deactivate():
        pass