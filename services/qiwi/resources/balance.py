from services.qiwi.models.balance import BalanceResponse
from utils.clients.http_client import HttpClient
from utils.config_reader import ConfigNamespace
from typing import Optional


class Balance:
    def __init__(self, client: HttpClient, user_data: Optional[ConfigNamespace] = None) -> None:
        self.client = client
        self.user_data = user_data

    def get_balance(self, expected_response_code: int = 200) -> BalanceResponse:
        """
        Получить список балансов кошелька.

        Returns:
            BalanceResponse: Список счетов с балансами.
        """
        resp = self.client.get(
            endpoint=f"v1/accounts/current",
            expected_response_code=expected_response_code,
        )
        return BalanceResponse(**resp)
