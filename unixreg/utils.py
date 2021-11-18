
def strict_types(function):
    def _decorator(*args, **kwargs):
        hints = function.__annotations__
        all_args = kwargs.copy()
        all_args.update(dict(zip(function.__code__.co_varnames, args)))
        for argument, argument_type in [(i, type(j)) for i, j in all_args.items()]:
            if argument in hints:
                if argument_type != hints[argument]:
                    raise TypeError('{} is not {}'.format(argument, hints[argument].__name__))
        result = function(*args, **kwargs)
        return result
    return _decorator
