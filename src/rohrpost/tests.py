import json
from typing import Any, List


class Consumer:
    def __init__(self) -> None:
        self.data: List[Any] = []
        self.closed = False

    def send(self, message: str) -> None:
        if not self.closed:
            self.data.append(json.loads(message))

    def close(self) -> None:
        self.closed = True
