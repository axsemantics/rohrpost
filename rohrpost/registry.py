from typing import Callable, Dict, List, Union

HANDLERS: Dict[str, Callable] = {}


def _rohrpost_handler(func: Callable, name: Union[str, List[str]]) -> Callable:
    def update_registry(key: str, value: Callable) -> None:
        if key in HANDLERS:
            raise Exception('Handler for "{}" is already defined.'.format(key))
        HANDLERS[key] = value

    name = name or func.__name__

    if isinstance(name, list):
        for n in name:
            update_registry(n, func)
    else:
        update_registry(name, func)
    return func


def rohrpost_handler(
    name: Union[str, List[str]] = ""
) -> Callable[[Callable], Callable]:
    def wrap(f: Callable) -> Callable:
        return _rohrpost_handler(f, name)

    return wrap
