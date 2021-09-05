import os
import subprocess

from subprocess import Popen, PIPE, STDOUT


class SecureStorage:
    """ Helper class for LUKS stuff """

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.mapping = f"/dev/mapper/{name}"

    def active(self) -> bool:
        """ Returns True if the luks volume is active """
        return os.path.exists(self.mapping)

    def exists(self) -> bool:
        """ Returns True if the path exists """
        return os.path.exists(self.path)

    def activate(self, password) -> bool:
        """ Activate storage with the given password """
        if self.active():
            return True

        # Send the password to cryptsetup 
        p = Popen(['/usr/bin/sudo', '/usr/sbin/cryptsetup', 'luksOpen', self.path, self.name, '-d', '-'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        p.communicate(password.encode())

        return p.returncode == 0

    def deactivate(self):
        """ Deactivate the mapping """
        if not self.active():
            return        
        subprocess.run(f"/usr/bin/sudo /usr/sbin/cryptsetup luksClose {self.name}", shell=True, check=True)

    def init(self, password):
        """ Reinitialize storage with a new password """      
        if self.active():
            print(f"Deactivate {self.name} first")
            return

        # Format the LUKS container
        subprocess.run(f'echo "{password}"| /usr/bin/sudo /usr/sbin/cryptsetup -q luksFormat {self.path}', shell=True, check=True)

        # Activate it
        self.activate(password)

        # Format it
        subprocess.run(f"/usr/bin/sudo /usr/sbin/mkfs.vfat -n SECURE {self.mapping}", shell=True, check=True)

        # Deactivate it
        self.deactivate()
