#!/usr/bin/env python3
"""Main module for the command line interface."""
import subprocess
from getpass import getpass

from cmd import Cmd

from .secure_storage import SecureStorage


def open_rw():
    """Open mount as read/writable."""
    subprocess.run("/usr/bin/sudo /usr/bin/mount -o remount,rw /", shell=True, check=True)


def close_rw():
    """Remount mount as read-only."""
    subprocess.run("/usr/bin/sudo /usr/bin/mount -o remount,ro /", shell=True, check=True)


def get_new_password():
    """Get the user's new password."""
    passwd1 = getpass(prompt="New Password: ")
    passwd2 = getpass(prompt="Verify New Password: ")

    if passwd1 != passwd2:
        return None

    return passwd1


class MainPrompt(Cmd):
    """The main command prompt."""

    prompt = "USBHonk> "
    intro = "Welcome! Type ? to list commands"
    secure_storage = SecureStorage("/dev/mmcblk0p3", "secure")

    def do_shell(self, _inp: str):
        """
        Drop to a shell.

        :raises CalledProcessError: If we can't run /bin/bash
        """
        subprocess.check_call(["/bin/bash"], shell=True)

    def do_secure_storage(self, inp: str):
        """
        Set up the secure storage.

        secure_storage [command]
        Configure Secure Storage
        Valid commands:
            init
            open
            close
        """
        if inp == "init":
            print("This will reinitialize your secure storage. ")
            print("All data will be erased.")
            if not input("Are you SURE? Type YES to continue: ") == "YES":
                return

            passwd = get_new_password()
            if not passwd:
                return

            self.secure_storage.init(passwd)

        elif inp == "open":
            passwd = getpass(prompt="Password: ")
            if not passwd:
                return
            if self.secure_storage.activate(passwd):
                print("Success")
            else:
                print("Failed to unlock")

        elif inp == "close":
            self.secure_storage.deactivate()

    def do_WIFI(self, _inp: str):
        """Wifi setup."""

    def do_EOF(self, inp: str):
        """Handle end-of-file (exit the shell)."""
        return self.do_exit(inp)

    def do_quit(self, inp: str):
        """Handle quit (exit the shell)."""
        return self.do_exit(inp)

    def do_exit(self, _inp: str):
        """Exit the shell."""
        print("Bye")
        return True


if __name__ == "__main__":
    MainPrompt().cmdloop()
