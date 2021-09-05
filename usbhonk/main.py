#!/usr/bin/env python3

from .secure_storage import SecureStorage

import subprocess

from cmd import Cmd
from getpass import getpass

def open_rw():
   subprocess.run("/usr/bin/sudo /usr/bin/mount -o remount,rw /", shell=True, check=True)

def close_rw():
   subprocess.run("/usr/bin/sudo /usr/bin/mount -o remount,ro /", shell=True, check=True)

def get_new_password():
    passwd1 = getpass(prompt="New Password: ")
    passwd2 = getpass(prompt="Verify New Password: ")

    if passwd1 != passwd2:
        return None

    return passwd1

class MainPrompt(Cmd):
    prompt = "USBHonk> "
    intro = "Welcome! Type ? to list commands"
    secure_storage = SecureStorage("/dev/mmcblk0p3", "secure")

    def do_shell(self, inp):
        """shell
        Drop to a shell"""
        subprocess.run("/bin/bash", shell=True, check=True)

    def do_secure_storage(self, inp):
        """secure_storage [command]
        Configure Secure Storage
        Valid commands:
            init
            open
            close"""

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
        

    def do_WIFI(self, inp):
        pass

    def do_EOF(self, inp):
        return self.do_exit(inp)

    def do_quit(self, inp):
        return self.do_exit(inp)

    def do_exit(self, inp):
        print("Bye")
        return True

if __name__ == "__main__":
    MainPrompt().cmdloop()