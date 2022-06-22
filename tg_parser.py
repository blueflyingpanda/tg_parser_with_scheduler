import json

from tg_app_info import TelegramAppInfo
from typing import List, Optional, Union, Set
from pathlib import Path
from abc import ABC, abstractmethod
from tg_msg import TelegramMessageInfo
from datetime import datetime
from telethon import TelegramClient
from time import time
from os.path import exists
from json import load, dump


class TelegramChatParser(ABC):

    """Chat parser that parse all messages that has keyword from chat for a given period of time"""

    def __init__(self, app_info: TelegramAppInfo, chat_name: str, keywords: Set[str]) -> None:
        self._chat_name = chat_name
        self._keywords = keywords
        self._messages: List[TelegramMessageInfo] = []
        self._client = TelegramClient(app_info.session, app_info.api_id, app_info.api_hash)
        self._client.start()

    def __del__(self):
        self._client.disconnect()

    def parse(self, period_in_seconds):

        LIMIT = 100
        last_msg_time_in_seconds = None
        current_time_in_seconds = time()

        for keyword in self.keywords:
            while not last_msg_time_in_seconds or last_msg_time_in_seconds > current_time_in_seconds - period_in_seconds:
                offset = 0
                for message in self._client.iter_messages(self._chat_name, limit=LIMIT, search=keyword, offset_id=offset):
                    self._messages.append(
                        TelegramMessageInfo(sender=message.sender, text=message.text, _id = message.id, date = datetime.timestamp(message.date))
                        )
                last_message = self._messages[-1]
                offset = last_message._id
                last_msg_time_in_seconds = last_message.date

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @property
    def keywords(self) -> Set[str]:
        return self._keywords

    @keywords.setter
    def keywords(self, val: Set[str]) -> None:
        self._keywords = val

    @property
    def chat_name(self) -> str:
        return self._chat_name

    @chat_name.setter
    def chat_name(self, val: str) -> None:
        self._chat_name = val

class TelegramChatParserToCsv(TelegramChatParser):

    """TelegramChatParser implementation that saves to CSV table"""

    def __init__(self, app_info: TelegramAppInfo, chat_name: str, keywords: Set[str], table_path: Optional[Union[Path, str]]) -> None:
        super().__init__(app_info, chat_name, keywords)
        self._table_path = table_path

    def save(self, *args, **kwargs):
        file_is_empty = False
        if not exists(self._table_path):
            file_is_empty = True
        with open(self._table_path, 'a') as file:
            if file_is_empty:
                file.write("username,first_name,last_name,phone,message_text\n")
            for message in self._messages:
                file.write(f'{message.sender.username},{message.sender.first_name},{message.sender.last_name},{message.sender.phone},"{message.text}"\n')


class TelegramChatParserToCsvStatistics(TelegramChatParser):

    """TelegramChatParser implementation that saves statistics to CSV"""

    def __init__(self, app_info: TelegramAppInfo, chat_name: str, keywords: Set[str],
                 table_path: Optional[Union[Path, str]],
                 json_path: Optional[Union[Path, str]]) -> None:
        super().__init__(app_info, chat_name, keywords)
        self._table_path = table_path
        self._json_path = json_path
        self._statistics = {}

    def parse(self, period_in_seconds):

        LIMIT = 100
        last_msg_time_in_seconds = None
        current_time_in_seconds = time()

        for chat in self._client.iter_dialogs():  # ISSUE doesn't find required chat without it
            print(chat.name)

        for keyword in self.keywords:
            offset = 0
            while not last_msg_time_in_seconds or last_msg_time_in_seconds > current_time_in_seconds - period_in_seconds:
                for message in self._client.iter_messages(self._chat_name, limit=LIMIT, search=keyword, offset_id=offset):
                    user_id = str(message.sender.id)
                    if user_id in self._statistics:
                        self._statistics[user_id]["points"] += 1
                    else:
                        self._statistics[user_id] = {"username": message.sender.username, "points": 1}
                    self._messages.append(
                        TelegramMessageInfo(sender=message.sender, text=message.text, _id = message.id, date = datetime.timestamp(message.date))
                        )
                    print(self._statistics)
                last_message = self._messages[-1]
                previous_offset = offset
                offset = last_message._id
                last_msg_time_in_seconds = last_message.date
                if previous_offset == offset:
                    break

    def save(self, interval: int):
        if not exists(self._json_path):
            with open(self._json_path, 'w') as file:
                dump({}, file)
        with open(self._json_path) as file:
            chat_data = load(file)
        last_update_time = chat_data.pop("last_update_time", 0)
        if time() > last_update_time + interval:
            for k in chat_data:
                chat_data[k]["points"] += self._statistics.get(k, {}).get("points", 0)
            for k in self._statistics:
                if k not in chat_data:
                    chat_data[k] = self._statistics[k]
            with open(self._table_path, 'w') as file:
                file.write("id,username,points\n")
                for k, v in chat_data.items():
                    file.write(f'{k},{v["username"]},{v["points"]}\n')
            with open(self._json_path, 'w') as file:
                chat_data["last_update_time"] = time()
                dump(chat_data, file)
        self._statistics.clear()
        self._messages.clear()
