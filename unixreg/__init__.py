"""
__init__
"""

__version__ = "0.1.1"


# upwards compatibility with winreg
try:
    from winreg import *
except ImportError:
    from unixreg.functions import *
    from unixreg.constants import *
    from unixreg.key import *
