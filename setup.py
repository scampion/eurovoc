import re

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

version = "1.0.0"

setup(
    name="eurovoc",
    version=version,
    description="Extract EuroVoc from the EU website",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Sebastien Campion",
    license="MIT",
    packages=['eurovoc'],
    install_requires=open("requirements.txt").read().splitlines(),
)
