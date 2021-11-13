import os
from copy import deepcopy
from typing import TypeVar, Union

from .constants import STANDARD_RIGHTS_REQUIRED

RegKeyT = TypeVar("RegKeyT", bound="RegKey")

_HANDLE_COUNTER = 0

class RegKey:

    def __init__(self, key: str = "", access: int = STANDARD_RIGHTS_REQUIRED):
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

        return None

    def __enter__(self) -> RegKeyT:
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return __class__.__name__

    def __str__(self):
        return f"{__class__.__name__}({self.key}, {self.handle}, {self.access})"

    def Close(self):
        pass

    def Detach(self):
        pass


PyHKEY = RegKey