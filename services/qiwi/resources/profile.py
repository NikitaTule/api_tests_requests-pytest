from typing import Optional

from services.qiwi.models.profile import ProfileResponse
from utils.clients.http_client import HttpClient
from utils.config_reader import ConfigNamespace


class ProfileResource:
    """Обёртки над эндпоинтами профиля пользователя."""

    def __init__(self, client: HttpClient, user_data: Optional[ConfigNamespace] = None) -> None:
        self.client = client
        self.user_data = user_data

    def get_profile(
            self,
            expected_response_code: int = 200,
    ) -> ProfileResponse:
        """
        Получить профиль пользователя.

        Args:
            expected_response_code: Ожидаемый HTTP статус код, по умолчанию 200.

        Returns:
            ProfileResponse: Типизированный ответ с authInfo, contractInfo, userInfo.
        """
        resp = self.client.get(
            endpoint="person-profile/v1/profile/current",
            expected_response_code=expected_response_code,
        )
        return ProfileResponse(**resp)
