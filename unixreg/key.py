from copy import deepcopy
from typing import Union

_HANDLE_COUNTER = 0

class RegKey:

	def __init__(self):
		pass

	def __add__(self, other: Union[str]):
		if isinstance(other, __class__):
			other = other.key

		if isinstance(other, str):
			retval = deepcopy(self)
			retval.key = f"{self.key}/{other}"

		return None

	def __enter__(self):
		pass

	def __exit__(self):
		pass

	def Close(self):
		pass

	def Detach(self):
		pass


PyHKEY = RegKey