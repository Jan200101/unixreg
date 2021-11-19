"""
Utilities
"""
from typing import get_args

def strict_types(function):
    """
    enforce type hinting on functions
    """

    def _decorator(*args, **kwargs):
        hints = function.__annotations__
        all_args = kwargs.copy()
        all_args.update(dict(zip(function.__code__.co_varnames, args)))
        for argument, argument_type in [(i, type(j)) for i, j in all_args.items()]:
            if (argument in hints and
               argument_type != hints[argument]
               and not isinstance(argument, get_args(hints[argument]))):
                raise TypeError(f"{argument} is not {hints[argument]}")

        return function(*args, **kwargs)

    return _decorator
