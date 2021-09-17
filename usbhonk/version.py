"""USBHonk version file."""
from pathlib import Path


version = open(Path(__file__).parent / 'VERSION', 'r').readline()
