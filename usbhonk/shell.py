import os

from pypsi.shell import Shell
from pypsi.commands.echo import EchoCommand
from pypsi.commands.exit import ExitCommand
from pypsi.commands.help import HelpCommand
from pypsi.commands.include import IncludeCommand
from pypsi.commands.macro import MacroCommand
from pypsi.commands.system import SystemCommand
from pypsi.plugins.comment import CommentPlugin
from pypsi.plugins.hexcode import HexCodePlugin
from pypsi.plugins.history import HistoryPlugin
from pypsi.plugins.multiline import MultilinePlugin
from pypsi.plugins.variable import VariablePlugin

from .commands import *
from .usb.gadgets.default_gadget import DefaultGadget


BANNER = '''
======================================================================================
  _    _  _____ ____       \x1b[1;31m_    _             _\x1b[0m
 | |  | |/ ____|  _ \\     \x1b[1;31m| |  | |           | |\x1b[0m
 | |  | | (___ | |_) |    \x1b[1;31m| |__| | ___  _ __ | | __\x1b[0m
 | |  | |\\___ \\|  _ <     \x1b[1;31m|  __  |/ _ \\| '_ \\| |/ /\x1b[0m
 | |__| |____) | |_) |    \x1b[1;31m| |  | | (_) | | | |   <\x1b[0m
  \\____/|_____/|____/     \x1b[1;31m|_|  |_|\\___/|_| |_|_|\_\\\x1b[0m


                                   ___
                               ,-""   `.
                             ,'  _   e )`-._  \x1b[1;32m/\x1b[0m
                            /  ,' `-._<.===-' \x1b[1;32m++==---\x1b[0m
                           /  /               \x1b[1;32m\\\x1b[0m
                          /  ;
              _          /   ;
 (`._    _.-"" ""--..__,'    |
 <_  `-""                     \\
  <`-                          :
   (__   <__.                  ;
     `-.   '-.__.      _.'    /
        \\      `-.__,-'    _,'
         `._    ,    /__,-'
            ""._\\__,'< <____
                 | |  `----.`.
                 | |        \\ `.
                 ; |___      \\-``
                 \\   --<
                  `.`.<
                    `-'
======================================================================================
'''


class HonkShell(Shell):
    # Base pypsi commands
    echo_cmd = EchoCommand()
    exit_cmd = ExitCommand()
    help_cmd = HelpCommand()
    include_cmd = IncludeCommand()
    macro_cmd = MacroCommand()
    system_cmd = SystemCommand(use_shell=True)
    comment_plugin = CommentPlugin()
    hexcode_plugin = HexCodePlugin()
    history_plugin = HistoryPlugin()
    multiline_plugin = MultilinePlugin()
    variable_plugin = VariablePlugin()

    bluetooth_cmd = BluetoothCommand()
    exploit_cmd = ExploitCommand()
    secure_storage_cmd = SecureStorageCommand()
    ssh_cmd = SshCommand()
    wifi_cmd = WifiCommand()


    def get_current_prompt(self):
        return f'\x1b[1;36mhonk \x1b[1;35m>\x1b[0m '

    def on_shell_ready(self):
        self.fallback_cmd = self.system_cmd
        self.ctx.default_gadget = DefaultGadget()
        print(BANNER)


if __name__ == '__main__':
    shell = HonkShell(width=os.get_terminal_size().columns)
    shell.cmdloop()
