from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


load_dotenv()


class ConfigNamespace:
    """Доступ к конфигурации через точку и []."""

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigNamespace(value))
            elif isinstance(value, list):
                setattr(
                    self,
                    key,
                    [ConfigNamespace(item) if isinstance(item, dict) else item for item in value],
                )
            else:
                setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' не имеет атрибута '{name}'")


class AppConfig:
    """Читает config.yaml и data/*.yaml, предоставляет доступ через атрибуты."""

    _instance = None

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        root = Path(__file__).parents[1]

        with (root / "config" / "config.yaml").open(encoding="utf-8") as f:
            config = yaml.safe_load(f)
        self.config = ConfigNamespace(config)

        config_dir = root / "config"
        for file_path in config_dir.rglob("*.yaml"):
            if file_path.name == "config.yaml":
                continue
            try:
                name = file_path.stem
                with file_path.open(encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                setattr(self, name, ConfigNamespace(data))
            except Exception as e:
                raise RuntimeError(f"Ошибка загрузки {file_path}: {e}")

    def get_service_host(self, service_name: str) -> str:
        """Получение хоста сервиса по имени."""
        return self.config.services[service_name]


app_config = AppConfig()
