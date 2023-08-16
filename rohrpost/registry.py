from typing import Callable, Dict, List, Union

HANDLERS: Dict[str, Callable] = {}


def _rohrpost_handler(func: Callable, name: Union[str, List[str]]) -> Callable:
    def update_registry(key: str, value: Callable) -> None:
        if key in HANDLERS:
            raise ValueError(f'Handler for "{key}" is already defined.')
        HANDLERS[key] = value

    name = name or func.__name__

    if isinstance(name, list):
        for _name in name:
            update_registry(_name, func)
    else:
        update_registry(name, func)
    return func


def rohrpost_handler(
    name: Union[str, List[str]] = ""
) -> Callable[[Callable], Callable]:
    def wrap(func: Callable) -> Callable:
        return _rohrpost_handler(func, name)

    return wrap
