import os
from typing import Union

from .key import RegKey
from .constants import STANDARD_RIGHTS_REQUIRED, KEY_WOW64_64KEY, KEY_WRITE, KEY_READ

KEY_TYPE = Union[str, RegKey]
SUBKEY_TYPE = KEY_TYPE | Union[None]

_KEY_CACHE = []
_ENV_REPLACE = {
    "USERPROFILE": os.getenv("HOME")
}

_CONFIG_DIR = os.getenv("XDG_CONFIG_HOME")
if not _CONFIG_DIR:
    _CONFIG_DIR = os.path.join(os.getenv("HOME"), ".config")
_CONFIG_DIR = os.path.join(_CONFIG_DIR, "unixreg")

def __init_values(key: KEY_TYPE, sub_key: SUBKEY_TYPE = None, access = STANDARD_RIGHTS_REQUIRED):
    if isinstance(key, str):
        key = RegKey(key)

    if sub_key:
        key = key + sub_key
    key.access = access

    return key

def __create_key(key: RegKey):
    path = os.path.join(_CONFIG_DIR, key.key)

    os.makedirs(path, exist_ok=True)

def CloseKey(key: RegKey):
    key.Close()

    try:
        _KEY_CACHE.remove(key)
    except ValueError:
        pass

def ConnectRegistry(computer: SUBKEY_TYPE, key: str):
    if not computer:
        return OpenKey(key, None)

    # ConnectRegistry is expected to throw an OSError on failure
    # any program that fails to catch this is to blame
    raise OSError("Not Implemented")

def OpenKeyEx(key: KEY_TYPE, sub_key: SUBKEY_TYPE, reserved=0, access=KEY_READ):
    return CreateKeyEx(key, sub_key, reserved, access)

OpenKey = OpenKeyEx

def CreateKey(key: KEY_TYPE, sub_key: SUBKEY_TYPE):
    return CreateKeyEx(key, sub_key)

def CreateKeyEx(key: KEY_TYPE, sub_key: SUBKEY_TYPE, reserved=0, access=KEY_WRITE):
    key = __init_values(key, sub_key, access)

    __create_key(key)

    _KEY_CACHE.append(key)

    return key


def DeleteKey(key: KEY_TYPE, sub_key: SUBKEY_TYPE):
    return DeleteKeyEx(key, sub_key)

def DeleteKeyEx(key: KEY_TYPE, sub_key: SUBKEY_TYPE, access=KEY_WOW64_64KEY, reserved=0):
    key = __init_values(key, sub_key, access)

    path = os.path.join(_CONFIG_DIR, key.key)
    if os.path.isfile(path):
        os.remove(path)

def DeleteValue(key: KEY_TYPE, value: str):
    key = __init_values(key)

    filepath = os.path.join(_CONFIG_DIR, key.key, value)
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

def EnumKey(key: KEY_TYPE, index: int):
    raise NotImplementedError("Not Implemented")

def EnumValue(key: KEY_TYPE, index: int):
    raise NotImplementedError("Not Implemented")

def ExpandEnvironmentStrings(env: str):
    for var in _ENV_REPLACE:
        env = env.replace(f"%{var}%", _ENV_REPLACE[var])
    env.replace("\\", os.path.sep)
    return env

def FlushKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")


def QueryInfoKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def QueryValueEx(key: KEY_TYPE, sub_key: SUBKEY_TYPE) -> str:
    key = __init_values(key, sub_key)

    filepath = os.path.join(_CONFIG_DIR, key.key)
    with open(filepath, "r") as file:
        return file.read()

QueryValue = QueryValueEx

def LoadKey(key: KEY_TYPE, sub_key: SUBKEY_TYPE, file_name: str):
    # Not Implemented but keeping this functionality stubbed should not cause a problem
    return

def SaveKey(key: KEY_TYPE, file_name: str) -> None:
    # Not Implemented but keeping this functionality stubbed should not cause a problem
    return

def SetValue(key: KEY_TYPE, sub_key: str, type: int, value: str):
    return SetValueEx(key, sub_key, 0, type, value)

def SetValueEx(key: KEY_TYPE, value_name: str, reserved: int, type: int, value: str) -> None:
    key = __init_values(key)

    filepath = os.path.join(_CONFIG_DIR, key.key, value_name)
    with open(filepath, "w") as file:
        file.write(value)

def DisableReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def EnableReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def QueryReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

