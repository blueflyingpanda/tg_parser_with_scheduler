from abc import ABC, abstractmethod
from json import dump, load
from dataclasses import dataclass
from typing import Optional, Union, Dict
from pathlib import Path


@dataclass
class TelegramAppInfo(ABC):

    """Structure that stores app info"""

    _id: Optional[str] = None
    _hash: Optional[str] = None
    session: str = "session"

    @abstractmethod
    def read_config(self, conf: Optional[Union[Path, str, Dict[str, str]]]) -> None:
        pass

    @property
    def api_id(self):
        if not self._id:
            raise ConfigNotRead()
        return self._id

    @property
    def api_hash(self):
        if not self._hash:
            raise ConfigNotRead()
        return self._hash


class ConfigNotRead(Exception):

    message = "Configuration file was not read!"


@dataclass
class TelegramAppInfoFromJson(TelegramAppInfo):

    """TelegramAppInfo implementation that receives path to json config as argument"""

    def read_config(self, conf="tg_id_and_hash.json") -> None:
        try:
            with open(conf) as file:
                conf_info = load(file)
            self._id = conf_info["api_id"]
            self._hash = conf_info["api_hash"]
        except KeyError as e:
            raise Exception(f"api id or api hash not in configuration file with path: {conf}")
        except FileNotFoundError as e:
            raise Exception(f"No configuration file with path: {conf}")
