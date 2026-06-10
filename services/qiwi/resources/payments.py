"""
Модуль ресурса платежей QIWI.
"""

from typing import Optional


from utils.clients.http_client import HttpClient
from utils.config_reader import ConfigNamespace


class Payments:
    """Обёртки над платёжными эндпоинтами QIWI."""

    def __init__(self, client: HttpClient, user_data: Optional[ConfigNamespace] = None) -> None:
        self.client = client
        self.user_data = user_data

    def get_payment_history(
        self,
        rows: int = 10,
        expected_response_code: int = 200,
    ) -> PaymentHistoryResponse:
        """
        Получить историю платежей кошелька.

        Args:
            rows: Количество записей в ответе, по умолчанию 10.
            expected_response_code: Ожидаемый HTTP статус код, по умолчанию 200.

        Returns:
            PaymentHistoryResponse: Список транзакций.
        """
        resp = self.client.get(
            endpoint=f"v1/persons/{self.user_data.wallet}/payments",
            url_payload={"rows": rows},
            expected_response_code=expected_response_code,
        )
        return PaymentHistoryResponse(**resp)

    def create_payment(
        self,
        to_wallet: str,
        amount: float = 1.0,
        currency: int = 643,
        comment: Optional[str] = None,
        expected_response_code: int = 200,
    ) -> CreatePaymentResponse:
        """
        Создать платёж на QIWI кошелёк.

        Args:
            to_wallet: Номер кошелька получателя.
            amount: Сумма перевода, по умолчанию 1.0 руб.
            currency: Код валюты, по умолчанию 643 (RUB).
            comment: Комментарий к платежу.
            expected_response_code: Ожидаемый HTTP статус код, по умолчанию 200.

        Returns:
            CreatePaymentResponse: Ответ с transaction.id и state.code.
        """
        body = {
            "id": str(int(__import__("time").time() * 1000)),
            "sum": {
                "amount": amount,
                "currency": str(currency),
            },
            "paymentMethod": {
                "type": "Account",
                "accountId": str(currency),
            },
            "fields": {
                "account": to_wallet,
            },
        }
        if comment:
            body["comment"] = comment

        resp = self.client.post(
            endpoint="sinap/api/v2/terms/99/payments",
            body_payload=body,
            expected_response_code=expected_response_code,
        )
        return CreatePaymentResponse(**resp)

    def get_transaction(
        self,
        txn_id: int,
        expected_response_code: int = 200,
    ) -> TransactionResponse:
        """
        Получить информацию о транзакции по ID.

        Args:
            txn_id: Идентификатор транзакции.
            expected_response_code: Ожидаемый HTTP статус код, по умолчанию 200.

        Returns:
            TransactionResponse: Данные транзакции со статусом.
        """
        resp = self.client.get(
            endpoint=f"v1/transactions/{txn_id}",
            expected_response_code=expected_response_code,
        )
        return TransactionResponse(**resp)