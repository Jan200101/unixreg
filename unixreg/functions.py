import os
from typing import Union

from .constants import *

KEY_TYPE = Union[str]

_KEY_CACHE = {}
_ENV_REPLACE = {
    "USERPROFILE": "HOME"
}

def CloseKey(key):
    pass

def ConnectRegistry(computer: Union[str, None], key: str):
    if not computer:
        return OpenKey(key, None)

    raise OSError("Not Implemented")

def CreateKey(key: KEY_TYPE, sub_key: Union[str, None]):
    return CreateKeyEx(key, sub_key)

def CreateKeyEx(key: KEY_TYPE, sub_key: Union[str, None], reserved=0, access=KEY_WRITE):
    pass

def DeleteKey(key: KEY_TYPE, sub_key: Union[str, None]):
    return DeleteKeyEx(key, sub_key)

def DeleteKeyEx(key: KEY_TYPE, sub_key: Union[str, None], access=KEY_WOW64_64KEY, reserved=0):
    pass

def DeleteValue(key: KEY_TYPE, value: str):
    pass

def EnumKey(key: KEY_TYPE, index: int):
    pass

def EnumValue(key: KEY_TYPE, index: int):
    pass

def ExpandEnvironmentStrings(env: str):
    """
    TODO Jan: correctly implement
    %HOME%/whatever => /home/sentry/whatever
    """
    return os.getenv(env)

def FlushKey(key: KEY_TYPE):
    pass

def LoadKey(key: KEY_TYPE, sub_key: Union[str, None], file_name: str):
    pass

def OpenKeyEx(key: KEY_TYPE, sub_key: Union[str, None], reserved=0, access=KEY_READ):
    pass

OpenKey = OpenKeyEx

def QueryInfoKey(key: KEY_TYPE):
    pass

def QueryValueEx(key: KEY_TYPE, sub_key: Union[str, None]):
    pass

QueryValue = QueryValueEx

def SaveKey(key: KEY_TYPE, file_name: str):
    pass

def SetValue(key: KEY_TYPE, sub_key: str, typei: int, value: str):
    return SetValueEx(key, sub_key, 0, typei, value)

def SetValueEx(key: KEY_TYPE, value_name: str, reserved: int, type: int, value: str):
    pass

def DisableReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def EnableReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def QueryReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

