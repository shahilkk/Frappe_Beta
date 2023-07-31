from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in beta_app/__init__.py
from beta_app import __version__ as version

setup(
	name="beta_app",
	version=version,
	description="demo",
	author="admin",
	author_email="shahilkhan.7139@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
