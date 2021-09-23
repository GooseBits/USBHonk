"""Setup script."""
import os
from pathlib import Path
from setuptools import setup

def load_requirements(filename):
    path = os.path.join(os.path.dirname(__file__), 'requirements', filename)
    return [line for line in open(path, 'r').readlines()
            if line.strip() and not line.startswith('#')]


requirements = load_requirements('requirements.txt')
dev_requirements = load_requirements('requirements-dev.txt')
version = open(Path(__file__).parent / 'usbhonk' / 'VERSION', 'r').readline()


setup(
    name='usbhonk',
    version=version,
    license='GPLv3',
    description='HOOOOOONK! Now for USB.',
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',
    author='GooseBits',
    author_email='contact@goosebits.io',
    # TODO: url='https://usbhonk.readthedocs.io/en/latest/',
    packages=['usbhonk', 'usbhonk.bluetooth', 'usbhonk.usb', 'usbhonk.usb.functions',
              'usbhonk.usb.gadgets', 'usbhonk.wifi', 'usbhonk.commands'],
    install_requires=requirements,
    include_package_data=True,
    extras_require={
        'dev': dev_requirements
    },
    project_urls={
        'Travis CI': 'https://app.travis-ci.com/github/GooseBits/USBHonk',
        # TODO: 'Documentation': 'https://usbhonk.readthedocs.io/en/latest/',
        'Source': 'https://github.com/GooseBits/USBHonk',
    },
    keywords=['USB', 'Honk'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ]
)
