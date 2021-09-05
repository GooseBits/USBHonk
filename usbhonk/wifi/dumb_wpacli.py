#!/secure/torpi/venv/bin/python3

import configparser
import subprocess
import sys

config = configparser.ConfigParser()
config.read("/secure/config/settings.ini")

ssid = config.get("wifi", "ssid", fallback=None)
psk = config.get("wifi", "password", fallback=None)

if not ssid:
    sys.exit(0)

for i in range(0, 20):
    subprocess.run(f"/usr/sbin/wpa_cli -i wlan0 remove_network {i}", shell=True, check=False, stdout=subprocess.DEVNULL)

result = subprocess.run("/usr/sbin/wpa_cli -i wlan0 add_network", shell=True, check=True, capture_output=True)
network_id = result.stdout.strip()

subprocess.run(f"/usr/sbin/wpa_cli -i wlan0 set_network {network_id} ssid '\"{ssid}\"'", shell=True, check=True)

if psk:
    subprocess.run(f"/usr/sbin/wpa_cli -i wlan0 set_network {network_id} psk '\"{psk}\"'", shell=True, check=True)
else:
    subprocess.run(f"/usr/sbin/wpa_cli -i wlan0 set_network {network_id} key_mgmt NONE", shell=True, check=True)

subprocess.run(f"/usr/sbin/wpa_cli -i wlan0 enable_network {network_id}", shell=True, check=True)
subprocess.run("/usr/sbin/wpa_cli -i wlan0 reconnect", shell=True, check=True)
