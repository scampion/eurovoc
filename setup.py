from datetime import datetime
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

now = datetime.now()
version = now.strftime("%y.%m.%d") + '.0'

setup(
    name="eurovoc",
    version=version,
    description="Extract EuroVoc from the EU website",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Sebastien Campion",
    license="MIT",
    packages=['eurovoc'],
    url='https://github.com/scampion/eurovoc',
    install_requires=open("requirements.txt").read().splitlines(),
)
