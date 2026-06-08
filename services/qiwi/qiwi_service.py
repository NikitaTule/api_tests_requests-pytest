from typing import Optional

from services.qiwi.resources.profile import ProfileResource
from utils.clients.http_client import HttpClient
from utils.config_reader import ConfigNamespace, app_config


class QiwiService:
    """Точка входа в сервис QIWI."""

    def __init__(
        self,
        user_data: Optional[ConfigNamespace] = None,
        headers: Optional[dict] = None,
    ) -> None:
        self.client = HttpClient(
            host=app_config.get_service_host("qiwi"),
            headers=headers or {},
        )
        self.user_data = user_data
        self.profile = ProfileResource(client=self.client, user_data=user_data)