"""Control wpa_cli via python."""
import re
import time
import subprocess


class WPAException(Exception):
    """Exception class thrown by :class:`WPACLIInterface` on error."""


class Network:
    """Representation for a single wireless network."""

    def __init__(self, bssid, freq, signal, flags, ssid):
        self.bssid = bssid
        self.freq = freq
        self.signal = signal
        self.ssid = ssid

        # Parse flags
        self.flags = re.findall(r"\[(.+?)\]", flags)
        self.encrypted = False
        for flag in self.flags:
            if any(x in flag for x in ["WPA", "WEP"]):
                self.encrypted = True
                break

    def __str__(self):
        return f"Network(ssid={self.ssid} freq={self.freq}"\
        f" signal={self.signal} encrypted={self.encrypted})"


class WPACliInterface:
    """Interface to wpa_cli."""

    def __init__(self, iface="wlan0"):
        self.iface = iface

    def connect(self, network) -> dict:
        """Connect to a network."""
        if network.encrypted:
            print("Cannot connect to encrypted network")
            return None
        self.disconnect()

        net_id = self._run_wpa_cli(["add_network"])
        self._run_wpa_cli(["set_network", net_id, "ssid", f'"{network.ssid}"'])
        self._run_wpa_cli(["set_network", net_id, "key_mgmt", "NONE"])
        self._run_wpa_cli(["enable_network", net_id])
        self._run_wpa_cli(["save_config"])
        self._run_wpa_cli(["reconfigure"])

        start_time = time.time()
        while True:
            # Sleep for a bit
            time.sleep(1)

            # Check if we're connected
            status = self.status()
            if status.get("wpa_state") == "COMPLETED":
                if "ip_address" in status:
                    return status

            # Give up eventually
            elapsed = time.time() - start_time
            if elapsed > 30:
                return None


    def disconnect(self):
        """Remove all networks from the wpa config."""
        lines = self._run_wpa_cli(["list_networks"]).split('\n')[1:]
        for line in lines:
            params = line.split("\t", maxsplit=3)
            if len(params) >= 3:
                net_id = params[0]
                self._run_wpa_cli(["remove_network", net_id])

    def status(self) -> dict:
        """Get the interface status."""
        lines = self._run_wpa_cli(["status"]).split('\n')
        result = {}
        for line in lines:
            line = line.strip()
            if line:
                key,val = line.split("=", maxsplit=1)
                result[key] = val
        return result

    def scan(self) -> list:
        """Scan for wireless networks."""
        self._run_wpa_cli(["scan"])
        time.sleep(5)
        lines = self._run_wpa_cli(["scan_results"]).split('\n')[1:]

        networks = []
        for line in lines:
            params = line.split('\t', maxsplit=4)
            if len(params) == 5:
                bssid = params[0]
                freq = int(params[1])
                signal = int(params[2])
                flags = params[3]
                ssid = params[4]
                networks.append(Network(bssid, freq, signal, flags, ssid))
        return networks

    def _run_wpa_cli(self, command) -> str:
        """Run a wpa_cli command and return the output."""
        args = ["/sbin/wpa_cli", "-i", self.iface]
        args.extend(command)
        result = subprocess.run(args=args,
            capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            err_str = f"Error calling {' '.join(args)}: {result.stdout.strip()}"
            raise WPAException(err_str)
        return result.stdout
