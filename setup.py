import sys
import setuptools

_SETUPTOOLS_MIN_VERSION = '30.3'

if setuptools.__version__ < _SETUPTOOLS_MIN_VERSION:
	print(f"version {_SETUPTOOLS_MIN_VERSION} is required")
	sys.exit(1)

setuptools.setup()
