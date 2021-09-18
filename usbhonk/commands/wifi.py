from typing import List
from getpass import getpass
from pypsi.completers import command_completer
from pypsi.core import Command, PypsiArgParser, CommandShortCircuit
from pypsi.shell import Shell
from pypsi.ansi import AnsiCodes

from usbhonk.control import unlock_device
from usbhonk.wifi.wpa import WPAConfig


class WifiCommand(Command):

    def __init__(self):
        self.parser = PypsiArgParser('wifi')
        action = self.parser.add_subparsers(dest='action')

        connect = action.add_parser('connect')
        connect.add_argument('ssid', help='network SSID')

        action.add_parser('scan')
        action.add_parser('disconnect')
        action.add_parser('status')

        super().__init__(name='wifi', brief='control wifi module',
                         usage=self.parser.format_usage())

    def setup(self, shell: Shell) -> None:
        shell.ctx.wpa_config = WPAConfig(iface="wlan0")

    def complete(self, shell, args, prefix):
        return command_completer(self.parser, shell, args, prefix, case_sensitive=True)

    def run(self, shell: Shell, params: List[str]) -> int:
        try:
            args = self.parser.parse_args(params)
        except CommandShortCircuit as err:
            return err.code

        if args.action == "connect":
            rc = self.connect(shell, args)
        elif args.action == 'disconnect':
            rc = self.disconnect(shell)
        elif args.action == 'scan':
            rc = self.scan()
        elif args.action == 'status':
            rc = self.status()

        return rc

    def connect(self, shell: Shell, ssid: str) -> int:
        passwd = getpass(prompt="Network Password: ")
        if not passwd:
            print("Warning. No password specified. Hopefully an open network...")

        with unlock_device():
            result = self.wpa_config.connect(ssid, passwd)

        if not result:
            self.error(shell, 'failed to connect')
            rc = -1
        else:
            print(result)
            rc = 0

        return rc

    def scan(self, shell: Shell) -> int:
        for network in shell.ctx.wpa_config.scan():
            print(network)
        return 0

    def disconnect(self, shell: Shell) -> int:
        shell.ctx.wpa_config.disconnect()
        return 0

    def status(self, shell: Shell) -> int:
        print(self.wpa_config.status())
        return 0
