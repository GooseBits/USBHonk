from pathlib import Path

class USBGadget:
    """ USB Gadget Base Class """
    def __init__(self, gadget_name):
        self.path = Path(f"/sys/kernel/config/usb_gadget/{gadget_name}")
        self.path.mkdir(parents=True)

    def __del__(self):
        if self.is_active():
            self.deactivate()
        # TODO: Unlink

    def active(self) -> bool:
        """ Returns true if the gadget is currently active """
        udc = self.path / "UDC"
        with udc.open() as f:
            return not not f.readline().strip()

    def activate(self):
        if self.active():
            return        

    def deactivate(self):
        if not self.active():
            return
