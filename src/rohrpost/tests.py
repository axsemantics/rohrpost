import json
from typing import Any


class Consumer:
    def __init__(self) -> None:
        self.data: list[Any] = []
        self.closed = False

    def send(self, message: str) -> None:
        if not self.closed:
            self.data.append(json.loads(message))

    def close(self) -> None:
        self.closed = True
