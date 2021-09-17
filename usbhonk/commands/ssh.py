from typing import List
import subprocess

from pypsi.core import Command, PypsiArgParser, CommandShortCircuit
from pypsi.shell import Shell
from pypsi.completers import command_completer

from usbhonk.control import unlock_device


class SshCommand(Command):

    def __init__(self):
        self.parser = PypsiArgParser()
        self.parser.add_argument('action', choices=('enable', 'disable'), action='store')

        super().__init__(name='ssh', brief='control the SSH service',
                         usage=self.parser.format_usage())

    def complete(self, shell: Shell, args: List[str], prefix: str) -> List[str]:
        return command_completer(self.parser, shell, args, prefix, case_sensitive=True)

    def run(self, shell: Shell, args: List[str]) -> int:
        try:
            args = self.parser.parse_args(args)
        except CommandShortCircuit as err:
            return err.code

        if args.action == 'enable':
            rc = self.enable(shell)
        elif args.action == 'disable':
            rc = self.disable(shell)

        return rc

    @unlock_device
    def enable(self, shell: Shell) -> int:
        return subprocess.check_call("systemctl enable --now ssh")

    def disable(self, shell: Shell) -> int:
        return subprocess.check_call("systemctl disable --now ssh")
