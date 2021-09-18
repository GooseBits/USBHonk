from typing import List
from pypsi.core import Command, PypsiArgParser, CommandShortCircuit
from pypsi.shell import Shell
from pypsi.completers import command_completer

from usbhonk.control import unlock_device
from usbhonk.bluetooth.bluetooth import Bluetooth


class BluetoothCommand(Command):

    def __init__(self):
        self.parser = PypsiArgParser('bluetooth')
        self.parser.add_argument('action', choices=('pair',))

        super().__init__(name='bluetooth', brief='control bluetooth module',
                         usage=self.parser.format_usage())

    def setup(self, shell: Shell) -> None:
        shell.ctx.bluetooth = Bluetooth(device="hci0")

    def complete(self, shell, args, prefix):
        return command_completer(self.parser, shell, args, prefix, case_sensitive=True)

    def run(self, shell: Shell, params: List[str]) -> int:
        try:
            args = self.parser.parse_args(params)
        except CommandShortCircuit as err:
            return err.code

        if args.action == "pair":
            rc = self.pair(shell)

        return rc

    @unlock_device
    def pair(self, shell: Shell) -> int:
        print("bluetooth: starting Bluetooth pairing...")
        shell.ctx.bluetooth.pair()
        return 0
