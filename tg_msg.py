from dataclasses import dataclass

@dataclass
class TelegramMessageInfo:

    sender: str
    text: str
    date: int
    _id: int