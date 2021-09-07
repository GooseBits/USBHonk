import subprocess
import sys

from subprocess import CalledProcessError


class Bluetooth:
    """ Class for pairing new bluetooth connections """

    def __init__(self, device="hci0"):
        self.device = device

    def pair(self):
        """ Pair a new device """
        self.discoverable = True
        subprocess.run([sys.executable, "-m", "usbhonk.bluetooth.agent", "--adapter", self.device])
        self.discoverable = False

    @property
    def discoverable(self) -> bool:
        try:
            msg = subprocess.check_output(["/usr/bin/hciconfig", self.device]).decode()
            return "PSCAN" in msg
        except CalledProcessError as exc:
            print(f"Failed to call hciconfig. {exc}")
            return False

    @discoverable.setter
    def discoverable(self, enabled: bool) -> None:
        if enabled:
            val = "piscan"
        else:
            val = "noscan"

        try:
            subprocess.check_output(["/usr/bin/hciconfig", self.device, val])
        except CalledProcessError as exc:
            print(f"Failed to set discoverable. {exc}")
