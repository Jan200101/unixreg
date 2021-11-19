import os
from tempfile import TemporaryDirectory
import pytest

from unixreg.constants import *
from unixreg.functions import *


_temp_dir = TemporaryDirectory()
os.environ["XDG_CONFIG_HOME"] = os.path.join(_temp_dir.name, "unixreg")

def test_ConnectRegistry():
    key = ConnectRegistry(None, HKEY_CURRENT_USER)
    key.Close()

    with pytest.raises(OSError):
        key = ConnectRegistry("FakeComputer", HKEY_CURRENT_USER)
        key.Close()

def test_CreateKey():
    def _create(key, subkey):
        with CreateKey(key, subkey) as key:
            CloseKey(key)

    _create(HKEY_CURRENT_USER, None)
    _create(HKEY_CURRENT_USER, "str")
    _create(HKEY_CURRENT_USER, RegKey("RegKey"))

    with pytest.raises(TypeError):
        _create(HKEY_CURRENT_USER, 1)
        _create(HKEY_CURRENT_USER, [])
        _create(HKEY_CURRENT_USER, ())
        _create(HKEY_CURRENT_USER, {})

def test_QueryValue():
    value = "value"
    value_name = "value_name"

    print(__import__("unixreg").HKEY_CURRENT_USER,)
    key = CreateKey(HKEY_CURRENT_USER, None)
    SetValue(key, value_name, REG_SZ, value)
    assert QueryValue(key, value_name) == value


def test_ExpandEnvironmentStrings():
    _test_str = "testvar"
    os.environ["TEST"] = _test_str
    os.environ["HOME"] = _test_str

    assert ExpandEnvironmentStrings(r"%TEST%") == os.environ["TEST"]
    assert ExpandEnvironmentStrings(r"%USERPROFILE%") == os.environ["HOME"]