from dataclasses import dataclass

@dataclass
class TelegramMessageInfo:

    sender: any
    text: str
    date: int
    _id: int
