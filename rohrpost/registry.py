HANDLERS = dict()


def _rohrpost_handler(func, name):
    def ret_func(*args, **kwargs):
        return func(*args, **kwargs)

    def update_registry(key, value):
        if key in HANDLERS:
            raise Exception('Handler for "{}" is already defined.'.format(key))
        HANDLERS[key] = value

    name = name or func.__name__

    if isinstance(name, list):
        for n in name:
            update_registry(n, func)
    else:
        update_registry(name, func)
    return ret_func


def rohrpost_handler(name=""):
    def wrap(f):
        return _rohrpost_handler(f, name)

    return wrap
