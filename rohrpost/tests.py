import json


class ReplyChannel:
    def __init__(self):
        self.data = []
        self.closed = False

    def send(self, message_dict):
        if not self.closed:
            self.data.append(json.loads(message_dict.get("text")))
            self.closed = message_dict.get("close", False)


class Message:
    def __init__(self):
        self.reply_channel = ReplyChannel()
