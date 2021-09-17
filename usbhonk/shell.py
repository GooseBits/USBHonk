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

from .commands.ssh import SshCommand


BANNER = '''
======================================================================================
 █████  █████  █████████  ███████████     █████   █████                     █████
░░███  ░░███  ███░░░░░███░░███░░░░░███   ░░███   ░░███                     ░░███
 ░███   ░███ ░███    ░░░  ░███    ░███    ░███    ░███   ██████  ████████   ░███ █████
 ░███   ░███ ░░█████████  ░██████████     ░███████████  ███░░███░░███░░███  ░███░░███
 ░███   ░███  ░░░░░░░░███ ░███░░░░░███    ░███░░░░░███ ░███ ░███ ░███ ░███  ░██████░
 ░███   ░███  ███    ░███ ░███    ░███    ░███    ░███ ░███ ░███ ░███ ░███  ░███░░███
 ░░████████  ░░█████████  ███████████     █████   █████░░██████  ████ █████ ████ █████
  ░░░░░░░░    ░░░░░░░░░  ░░░░░░░░░░░     ░░░░░   ░░░░░  ░░░░░░  ░░░░ ░░░░░ ░░░░ ░░░░░

                                                    ___
                                                ,-""   `.
                                              ,'  _   e )`-._   /
                                             /  ,' `-._<.===-'  ++==---
                                            /  /                \\
                                           /  ;
                               _          /   ;
                  (`._    _.-"" ""--..__,'    |
                  <_  `-""                     \\
                   <`-                          :
                    (__   <__.                  ;
                      `-.   '-.__.      _.'    /
                         \      `-.__,-'    _,'
                          `._    ,    /__,-'
                             ""._\__,'< <____
                                  | |  `----.`.
                                  | |        \ `.
                                  ; |___      \-``
                                  \   --<
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
    system_cmd = SystemCommand()
    comment_plugin = CommentPlugin()
    hexcode_plugin = HexCodePlugin()
    history_plugin = HistoryPlugin()
    multiline_plugin = MultilinePlugin()
    variable_plugin = VariablePlugin()

    ssh_cmd = SshCommand()

    def get_current_prompt(self):
        return f'\x1b[1;32musb-honk >\x1b[0m '

    def on_shell_ready(self):
        print(BANNER)


if __name__ == '__main__':
    shell = HonkShell(width=os.get_terminal_size().columns)
    shell.cmdloop()
