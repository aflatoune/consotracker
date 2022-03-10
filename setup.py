from setuptools import setup, find_packages
import os

VERSION = os.environ.get('VERSION', 'v0.0.0')

with open('requirements.txt', 'r', encoding='utf-8') as file:
    REQUIRED_PACKAGES = file.read()

setup(
    name="consotracker",
    version=VERSION,
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description=''
)