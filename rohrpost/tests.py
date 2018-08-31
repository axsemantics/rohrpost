import json


class Consumer:
    def __init__(self):
        self.data = []
        self.closed = False

    def send(self, message: str):
        if not self.closed:
            self.data.append(json.loads(message))

    def close(self):
        self.closed = True
