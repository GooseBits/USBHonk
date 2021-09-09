#!/usr/bin/env python3
"""Main module for the command line interface."""
from os import close
import subprocess
import time

from getpass import getpass

from cmd import Cmd

from usbhonk.bluetooth.bluetooth import Bluetooth
from usbhonk.usb.gadgets.default_gadget import DefaultGadget
from usbhonk.usb.gadgets.razer_attack import RazerAttack
from usbhonk.secure_storage import SecureStorage
from usbhonk.wifi.wpa import WPAConfig


def open_rw():
    """Open mount as read/writable."""
    subprocess.run("/usr/bin/mount -o remount,rw /", shell=True, check=True)


def close_rw():
    """Remount mount as read-only."""
    subprocess.run("/usr/bin/mount -o remount,ro /", shell=True, check=True)


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
    secure_storage = SecureStorage(path="/dev/mmcblk0p3", name="secure")
    wpa_config = WPAConfig(iface="wlan0")
    default_gadget = DefaultGadget()
    bluetooth = Bluetooth(device="hci0")

    def do_shell(self, _inp: str) -> None:
        """
        Drop to a shell.

        :raises CalledProcessError: If we can't run /bin/bash
        """
        subprocess.run("/bin/bash -i", shell=True, check=True)

    def do_ssh(self, inp: str) -> None:
        """
        Enable or disable SSH server on boot

        Valid commands:
            enable
            disable
        """
        if not inp:
            print("A command is required: ")
            print("enable\ndisable")
            return

        if inp == "enable":
            open_rw()
            try:
                subprocess.run("systemctl enable --now ssh", shell=True, check=True)
                print("SSH enabled!")
            except subprocess.CalledProcessError as exc:
                print(f"Failed to enable ssh: {exc}")
            finally:
                close_rw()
        elif inp == "disable":
            open_rw()
            try:
                subprocess.run("systemctl disable --now ssh", shell=True, check=True)
                print("SSH disabled!")
            except subprocess.CalledProcessError as exc:
                print(f"Failed to disable ssh: {exc}")
            finally:
                close_rw()
        else:
            print(f"Invalid input {inp}. Expected enable or disable")

    def do_exploit(self, inp: str) -> None:
        """
        Run an exploit

        Valid commands:
            razer
        """
        if not inp:
            print("A command is required: ")
            print("razer")
            return

        if inp == "razer":
            if self.default_gadget.lun1.file:
                print("Eject the secure disk from the host first")
                return

            # Deactivate our default gadget
            self.default_gadget.active = False

            # Activate the razer attack
            razer = RazerAttack()
            razer.active = True
            print("Razer attack active")

            time.sleep(20)

            # Return to normal
            print("Returning to normal")
            razer.active = False
            self.default_gadget.active = True

    def do_secure_storage(self, inp: str) -> None:
        """
        Set up the secure storage.

        secure_storage [command]
        Configure Secure Storage
        Valid commands:
            init
            open
            close
        """
        if not inp:
            print("A command is required: ")
            print("init\nopen\nclose")
            return

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
                # Now attach it as mass storage on lun1
                self.default_gadget.lun1.file = self.secure_storage.mapping
            else:
                print("Failed to unlock")

        elif inp == "close":
            if self.default_gadget.lun1.file:
                print("Eject the secure disk from the host first")
                return
            self.secure_storage.deactivate()
        else:
            print("Unknown subcommand")

    def do_bluetooth(self, inp: str) -> None:
        """
        Configure bluetooth connectivity

        bluetooth <command>

        Configure Bluetooth
        Valid commands:
            pair
        """
        if not inp:
            print("A command is required: ")
            print("pair")
            return

        toks = inp.split()
        cmd = toks[0]
        args = toks[1:]

        if len(args) > 0:
            print("No commands take arguments. Too many args.")
            return

        if cmd == "pair":
            print("Starting Bluetooth pairing...")
            open_rw()
            try:
                self.bluetooth.pair()
            finally:
                close_rw()

    def do_wifi(self, inp: str) -> None:
        """
        Set up the WiFi connection.

        WIFI <command> [ARG-1, ..., ARG-N]

        Configure Wifi
        Valid commands:
            scan
            connect <ssid>
            disconnect
            status
        """
        # TODO:
        if not inp:
            print("A command is required: ")
            print("scan\nconnect <ssid>\ndisconnect\nstatus")
            return

        toks = inp.split()
        cmd = toks[0]
        args = toks[1:]

        if len(args) > 1:
            print("No commands take more than one argument. Too many args.")
            return

        if cmd == "connect" and not args:
            print("connect requires 1 argument, the name of the network to connect to.")
            return

        # It's prob. valid at this point
        if cmd == "scan":
            for network in self.wpa_config.scan():
                print(network)
        elif cmd == "connect":
            passwd = getpass(prompt="Network Password: ")
            if not passwd:
                print("Warning. No password specified. Hopefully an open network...")

            open_rw()
            try:
                result = self.wpa_config.connect(args[0], passwd)
            finally:
                close_rw()

            if not result:
                print("Failed to connect")
            else:
                print(result)
        elif cmd == "disconnect":
            self.wpa_config.disconnect()
        elif cmd == "status":
            print(self.wpa_config.status())

    def do_EOF(self, inp: str) -> bool:
        """Handle end-of-file (exit the shell)."""
        return self.do_exit(inp)

    def do_quit(self, inp: str) -> bool:
        """Handle quit (exit the shell)."""
        return self.do_exit(inp)

    def do_exit(self, _inp: str) -> bool:
        """Exit the shell."""
        print("Bye")
        return True


if __name__ == "__main__":
    MainPrompt().cmdloop()
