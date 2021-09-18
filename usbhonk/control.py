import subprocess
from getpass import getpass
from contextlib import contextmanager

from pypsi.ansi import AnsiCodes


def open_rw():
    """Open mount as read/writable."""
    subprocess.check_call("/usr/bin/mount -o remount,rw /")


def close_rw():
    """Remount mount as read-only."""
    subprocess.check_call("/usr/bin/mount -o remount,ro /")


@contextmanager
def unlock_device(func: callable) -> callable:
    '''
    Decorator to  unlock the root filesystem for the duration of the function call.
    '''
    open_rw()
    try:
        yield
    finally:
        close_rw()


def get_new_password():
    """Get the user's new password."""
    passwd1 = getpass(prompt="New Password: ")
    passwd2 = getpass(prompt="Verify New Password: ")

    if passwd1 != passwd2:
        print(AnsiCodes.red('error: passwords do not match'))
        return None

    return passwd1
