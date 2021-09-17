import subprocess

def open_rw():
    """Open mount as read/writable."""
    subprocess.check_call("/usr/bin/mount -o remount,rw /")


def close_rw():
    """Remount mount as read-only."""
    subprocess.check_call("/usr/bin/mount -o remount,ro /")


def unlock_device(func: callable) -> callable:
    '''
    Decorator to  unlock the root filesystem for the duration of the function call.
    '''
    def wrapper(*args, **kwargs):
        open_rw()
        try:
            ret = func()
        finally:
            close_rw()

        return ret

    return wrapper
