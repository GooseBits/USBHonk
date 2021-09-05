"""USB Gadget code."""
from pathlib import Path


class USBGadget:
    """USB Gadget Base Class."""

    def __init__(self, name):
        """Create a :class:`USBGadget`."""
        self.path = Path(f"/sys/kernel/config/usb_gadget/{name}")
        self.path.mkdir(parents=True)

    def __del__(self):
        """Handle cleanup."""
        if self.is_active():
            self.deactivate()
        # TODO: Unlink

    def is_active(self) -> bool:
        """Check if it's active."""

    def activate(self):
        """Activate the USB gadget."""

    def deactivate(self):
        """Deactivate the USB gadget."""
