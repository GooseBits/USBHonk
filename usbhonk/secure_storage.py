"""Handle secure storage."""
import os
import subprocess
import time

from subprocess import CalledProcessError, Popen, PIPE


class SecureStorage:
    """Helper class for LUKS stuff."""

    def __init__(self, path: str, name: str):
        """Create the :class:`SecureStorage` object."""
        self.path = path
        self.name = name
        self.mapping = f"/dev/mapper/{name}"

    def active(self) -> bool:
        """Return True if the luks volume is active."""
        return os.path.exists(self.mapping)

    def exists(self) -> bool:
        """Return True if the path exists."""
        return os.path.exists(self.path)

    def activate(self, password: str) -> bool:
        """Activate storage with the given password."""
        if self.active():
            return True

        # Send the password to cryptsetup
        cmd = ['/usr/sbin/cryptsetup', 'luksOpen', self.path, self.name, '-d', '-']
        with Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
            output, err = proc.communicate(password.encode())
            if proc.returncode != 0:
                print(f"luksOpen returned {proc.returncode}", output, err)
                return False
            return True

    def deactivate(self) -> bool:
        """Deactivate the mapping."""
        if not self.active():
            return True
        try:
            subprocess.check_call(["/usr/sbin/cryptsetup", "luksClose", self.name])
        except CalledProcessError as exc:
            print(f"Failed to call luksClose. {exc}")
            return False

        return True

    def init(self, password: str) -> None:
        """Reinitialize storage with a new password."""
        if self.active():
            print(f"Deactivate {self.name} first")
            return

        # Format the LUKS container
        cmd = ['/usr/sbin/cryptsetup', '-q', 'luksFormat', self.path]
        with Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
            output, err = proc.communicate(password.encode())
            if proc.returncode != 0:
                print(f"luksFormat returned {proc.returncode}", output, err)
                return

        # Activate it
        if not self.activate(password):
            print(f"Failed to activate {self.mapping}")
            return

        # Format it
        try:
            subprocess.check_call(["/usr/sbin/mkfs.vfat", "-n", "SECURE", self.mapping])
            os.sync()
            time.sleep(2)
        except CalledProcessError as exc:
            print(f"Failed to format. {exc}")
        finally:
            # Deactivate it
            self.deactivate()

