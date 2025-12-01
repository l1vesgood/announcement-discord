import json
import os
from dataclasses import dataclass
from typing import List, Union


@dataclass
class ChannelConfig:
    name: str
    emoji: str
    description: str
    id: int
    auto_reactions: List[str]
    rules: str
    format: Union[str, List[str]]
    contacts: bool = False


class Config:
    """Класс для управления конфигурацией приложения"""

    def __init__(self, config_name: str = "config.json") -> None:
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, config_name)
        self._config = {}
        self._load_config()

    def _load_config(self) -> None:
        """Загружает конфигурацию из файла"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфигурации не найден: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Ошибка парсинга JSON в файле: {self.config_path}")

    @property
    def player_role_id(self) -> int:
        return self._config.get("player_role_id")

    @property
    def guild_id(self) -> int:
        return self._config.get("guild_id")

    @property
    def channels(self) -> List[ChannelConfig]:
        """Возвращает список конфигураций каналов"""
        channels_data = self._config.get("channels", [])
        return [ChannelConfig(**c) for c in channels_data]


config = Config()
