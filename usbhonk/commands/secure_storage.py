from typing import List
from getpass import getpass
from pypsi.core import Command, PypsiArgParser, CommandShortCircuit
from pypsi.shell import Shell
from pypsi.ansi import AnsiCodes
from pypsi.completers import command_completer

from usbhonk.control import get_new_password
from usbhonk.secure_storage import SecureStorage


class SecureStorageCommand(Command):

    def __init__(self):
        self.parser = PypsiArgParser('secure-storage')
        self.parser.add_argument('action', choices=('init', 'open', 'close'))

        super().__init__(name='secure-storage', brief='control secure storage module',
                         usage=self.parser.format_usage())

    def setup(self, shell: Shell) -> None:
        shell.ctx.secure_storage = SecureStorage(path="/dev/mmcblk0p3", name="secure")

    def complete(self, shell, args, prefix):
        return command_completer(self.parser, shell, args, prefix, case_sensitive=True)

    def run(self, shell: Shell, params: List[str]) -> int:
        try:
            args = self.parser.parse_args(params)
        except CommandShortCircuit as err:
            return err.code

        if args.action == "init":
            rc = self.init_secure_storage(shell)
        elif args.action == "open":
            rc = self.open_secure_storage(shell)
        elif args.action == "close":
            rc = self.close_secure_storage(shell)

        return rc

    def init_secure_storage(self, shell: Shell):
        print(AnsiCodes.yellow("This will reinitialize your secure storage"))
        print(AnsiCodes.yellow("All data will be erased"))
        print()
        if not input("Are you SURE? Type YES to continue: ") == "YES":
            return

        passwd = get_new_password()
        if not passwd:
            return 1

        shell.ctx.secure_storage.init(passwd)
        return 0

    def open_secure_storage(self, shell: Shell) -> int:
        passwd = getpass(prompt="Password: ")
        if not passwd:
            return

        if shell.ctx.secure_storage.activate(passwd):
            print(AnsiCodes.green("secure-storage: success"))
            # Now attach it as mass storage on lun1
            shell.ctx.default_gadget.lun1.file = shell.ctx.secure_storage.mapping
            rc = 0
        else:
            print("Failed to unlock")
            rc = -1

        return rc

    def close_secure_storage(self, shell: Shell) -> int:
        if shell.ctx.default_gadget.lun1.file:
            self.error(shell, "eject the secure disk from the host first")
            return -1
        shell.ctx.secure_storage.deactivate()
