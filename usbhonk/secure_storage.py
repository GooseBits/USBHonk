"""Handle secure storage."""
import os
import subprocess

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
        cmd = ['/usr/bin/sudo', '/usr/sbin/cryptsetup', 'luksOpen', self.path, self.name, '-d', '-']
        with Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
            proc.communicate(password.encode())
            return proc.returncode == 0

    def deactivate(self) -> None:
        """Deactivate the mapping."""
        if not self.active():
            return
        subprocess.check_call(["/usr/bin/sudo", "/usr/sbin/cryptsetup", "luksClose", self.name], shell=True)

    def init(self, password: str) -> None:
        """Reinitialize storage with a new password."""
        if self.active():
            print(f"Deactivate {self.name} first")
            return

        # Format the LUKS container
        try:
            subprocess.run(
                f'echo "{password}"| /usr/bin/sudo /usr/sbin/cryptsetup -q luksFormat {self.path}',
                shell=True, check=True)
        except CalledProcessError as exc:
            print(f"Failed to format (luksFormat). {exc}")
            return

        # Activate it
        self.activate(password)

        # Format it
        try:
            subprocess.check_call(["/usr/bin/sudo", "/usr/sbin/mkfs.vfat", "-n", "SECURE", self.mapping], shell=True)
        except CalledProcessError as exc:
            print(f"Failed to format. {exc}")
            self.deactivate()
            return

        # Deactivate it
        self.deactivate()
