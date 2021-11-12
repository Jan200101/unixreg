__version__ = "0.1.0"


# upwards compatibility with winreg
try:
	from winreg import *
except ImportError:
	from .functions import *
	from .constants import *
	from .key import *
