from setuptools import setup, find_packages


with open('requirements.txt', 'r', encoding='utf-8') as file:
    REQUIRED_PACKAGES = file.read()

setup(
    name="consotracker",
    version='0.1.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description=''
)