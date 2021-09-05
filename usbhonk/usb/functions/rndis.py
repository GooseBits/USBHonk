from .function import USBFunction

class RNDIS(USBFunction):
    """ Network adapter supported by Windows """

    def __init__(self, gadget_path, rndis_name):
        super().__init__(gadget_path, f"rndis.{rndis_name}")

    def dev_addr(self) -> str:
        """ Get the device MAC address """
        p = self.path / "dev_addr"
        return p.open().readline()

    def dev_addr(self, addr) -> str:
        """ Set the device MAC address """
        p = self.path / "dev_addr"
        with p.open() as f:
            f.write(addr)

    def host_addr(self) -> str:
        """ Get the host MAC address """
        p = self.path / "host_addr"
        return p.open().readline()

    def dev_addr(self, addr) -> str:
        """ Set the host MAC address """
        p = self.path / "host_addr"
        with p.open() as f:
            f.write(addr)
