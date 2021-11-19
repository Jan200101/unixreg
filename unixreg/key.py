# pylint: disable=invalid-name, global-statement
"""
Implements anything related to the Registry Handle
"""
import os
from copy import deepcopy
from typing import TypeVar, Union

RegKeyT = TypeVar("RegKeyT", bound="RegKey")

_HANDLE_COUNTER = 0

class RegKey:
    """
    Implementation of the Registry Handle
    https://docs.python.org/3/library/winreg.html#registry-handle-objects
    """

    key = ""
    handle = 0
    access = 0

    def __init__(self, key: str = "", access: int = 1):
        global _HANDLE_COUNTER
        _HANDLE_COUNTER += 1

        self.key = key
        self.handle = _HANDLE_COUNTER
        self.access = access

    def __add__(self, other: Union[str, RegKeyT]) -> RegKeyT:
        if isinstance(other, __class__):
            other = other.key

        if isinstance(other, str):
            other = other.replace("\\\\", "\\").replace("\\", os.path.sep)
            retval = deepcopy(self)
            retval.key = os.path.join(self.key, other)
            return retval

        raise TypeError("Invalid Type")

    def __enter__(self) -> RegKeyT:
        return self

    def __exit__(self, *args, **kwargs):
        self.Close()

    def __repr__(self):
        return __class__.__name__

    def __str__(self):
        return f"{__class__.__name__}(\"{self.key}\", {self.handle}, {self.access})"

    def Close(self):
        """
        Closes the key by cleaning up its values
        """

    def Detach(self) -> int:
        """
        Is suppose to detach the handle and give it to someone else,
        but we don't have that luxury
        """
        self.Close()
        return self.handle


PyHKEY = RegKey
