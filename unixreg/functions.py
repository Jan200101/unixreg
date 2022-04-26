# pylint: disable=invalid-name, unused-argument, unspecified-encoding, missing-function-docstring
"""
Implements all winreg functions

https://docs.python.org/3/library/winreg.html#functions
"""
import os
from typing import Union
from re import findall
from tempfile import TemporaryDirectory
from warnings import warn
from typing import Optional, List

from unixreg.key import RegKey
from unixreg.constants import STANDARD_RIGHTS_REQUIRED, KEY_WOW64_64KEY, KEY_WRITE, KEY_READ

KEY_TYPE = Union[str, RegKey]
SUBKEY_TYPE = Union[str, RegKey, None]

_KEY_CACHE: List[RegKey] = []
_ENV_REPLACE = {
    "USERPROFILE": "HOME"
}

_CONFIG_DIR = os.getenv("XDG_CONFIG_HOME")
if not _CONFIG_DIR:
    home = os.getenv("HOME")
    if home:
        _CONFIG_DIR = os.path.join(home, ".config")
    else:
        _CONFIG_DIR = TemporaryDirectory().name
        if not os.getenv("TOX"):
            warn(f"Could not find directory to put registry in. Falling back to {_CONFIG_DIR}")
_CONFIG_DIR = os.path.join(_CONFIG_DIR, "unixreg")

def __init_values(key: KEY_TYPE, sub_key: SUBKEY_TYPE = None, access = STANDARD_RIGHTS_REQUIRED):
    if isinstance(key, str):
        key = RegKey(key)

    if sub_key is not None:
        print(sub_key)
        key = key + sub_key
    key.access = access

    return key

def __create_key(key: RegKey):
    if _CONFIG_DIR and key and key.key:
        path = os.path.join(_CONFIG_DIR, key.key)

        os.makedirs(path, exist_ok=True)

def CloseKey(key: RegKey):
    """
    Closes a previously opened registry key.
    The key argument specifies a previously opened key.
    """
    key.Close()

    try:
        _KEY_CACHE.remove(key)
    except ValueError:
        pass

def ConnectRegistry(computer: Union[str, None], key: RegKey):
    """
    Opens a registry handle on another computer and returns the handle

    If computer_name is None, the local computer is used, otherwise
    OSError is raised to signify the function failing
    """
    if not computer:
        return OpenKey(key, None)
    raise OSError("Not Implemented")

def OpenKeyEx(key: RegKey, sub_key: SUBKEY_TYPE, reserved=0, access=KEY_READ):
    return CreateKeyEx(key, sub_key, reserved, access)

OpenKey = OpenKeyEx

def CreateKey(key: RegKey, sub_key: SUBKEY_TYPE):
    return CreateKeyEx(key, sub_key)

def CreateKeyEx(key: RegKey, sub_key: SUBKEY_TYPE, reserved=0, access=KEY_WRITE):
    key = __init_values(key, sub_key, access)

    __create_key(key)

    _KEY_CACHE.append(key)

    return key


def DeleteKey(key: KEY_TYPE, sub_key: SUBKEY_TYPE):
    return DeleteKeyEx(key, sub_key)

def DeleteKeyEx(key: KEY_TYPE, sub_key: SUBKEY_TYPE, access=KEY_WOW64_64KEY, reserved=0):
    kkey = __init_values(key, sub_key, access)

    if _CONFIG_DIR:
        path = os.path.join(_CONFIG_DIR, kkey.key)
        if os.path.isfile(path):
            os.remove(path)

def DeleteValue(key: KEY_TYPE, value: str):
    kkey = __init_values(key)

    if _CONFIG_DIR:
        filepath = os.path.join(_CONFIG_DIR, kkey.key, value)
        try:
            os.remove(filepath)
        except FileNotFoundError:
            pass

def EnumKey(key: KEY_TYPE, index: int):
    raise NotImplementedError("Not Implemented")

def EnumValue(key: KEY_TYPE, index: int):
    raise NotImplementedError("Not Implemented")

def ExpandEnvironmentStrings(env: str):
    for key, val in _ENV_REPLACE.items():
        env = env.replace(f"%{key}%", f"%{val}%")

    match = findall(r"%(.+?)%", env)

    for val in match:
        valenv = os.getenv(val)
        if valenv:
            env = env.replace(f"%{val}%", valenv)

    env.replace("\\", os.path.sep)
    return env

def FlushKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")


def QueryInfoKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def QueryValueEx(key: KEY_TYPE, sub_key: SUBKEY_TYPE) -> str:
    kkey = __init_values(key, sub_key)

    if _CONFIG_DIR:
        filepath = os.path.join(_CONFIG_DIR, kkey.key)
        with open(filepath, "r") as file:
            return file.read()

    return ""

QueryValue = QueryValueEx

def LoadKey(key: RegKey, sub_key: SUBKEY_TYPE, file_name: str):
    # this requires a win32 permission compatibility layer
    raise OSError("Not Implemented")

def SaveKey(key: RegKey, file_name: str) -> None:
    # this requires a win32 permission compatibility layer
    raise OSError("Not Implemented")

def SetValue(key: KEY_TYPE, sub_key: SUBKEY_TYPE, typearg: int, value: str) -> None:
    if isinstance(sub_key, RegKey):
        sub_key = sub_key.key

    if sub_key:
        return SetValueEx(key, sub_key, 0, typearg, value)

def SetValueEx(key: KEY_TYPE, value_name: str, reserved: int, typearg: int, value: str) -> None:
    kkey = __init_values(key)

    if _CONFIG_DIR:
        filepath = os.path.join(_CONFIG_DIR, kkey.key, value_name)
        with open(filepath, "w") as file:
            file.write(value)

def DisableReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def EnableReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")

def QueryReflectionKey(key: KEY_TYPE):
    raise NotImplementedError("Not Implemented")


# Non winreg functions
def LoadRegFile(file_name: str) -> Optional[str]:

    def _strip_quotes(val) -> str:
        _QUOTE_LIST = ("\"", '\'')
        if val.startswith(_QUOTE_LIST) and val.endswith(_QUOTE_LIST):
            val = val[1:-1]
        return val

    def _strip_brackets(val) -> str:
        _BRACKET_LIST = ("[", "]")
        if val.startswith(_BRACKET_LIST) and val.endswith(_BRACKET_LIST):
            val = val[1:-1]
        return val

    with open(file_name, "r") as reg:
        nextline = reg.readline()

        key: Optional[str] = None

        while nextline:
            line = nextline.strip()
            nextline = reg.readline()

            if len(line) == 1:
                continue

            split = line.split("=")

            keyline = _strip_brackets(line)
            if keyline:
                key = keyline
            elif key and len(split) == 2:
                name, value = split
                name = _strip_quotes(name)
                value = _strip_quotes(value)

                os.makedirs(key, exist_ok=True)

                if _CONFIG_DIR:
                    with open(os.path.join(_CONFIG_DIR, key, name), "w") as regvalue:
                        regvalue.write(value)

                print(f"[{key}] {name}={value}")

    return None