"""
Модуль базового HTTP клиента.
"""

import time
from json.decoder import JSONDecodeError
from typing import Dict, Optional, Union

import requests
import urllib3

from utils.logger import request_logger


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpClient:
    """Базовый HTTP клиент для работы с JSON API."""

    def __init__(
        self,
        host: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._host = host
        self._headers = headers.copy() if headers else {}

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        host: Optional[str] = None,
        data: Optional[Union[Dict, str]] = None,
        body_payload: Optional[Dict] = None,
        header_payload: Optional[Dict[str, str]] = None,
        url_payload: Optional[Dict] = None,
        files: Optional[Dict] = None,
        expected_response_code: int = 200,
        timeout: int = 90,
        allow_redirects: bool = True,
        is_binary: bool = False,
        return_cookies: bool = False,
        attempts: int = 1,
        retry_delay: float = 1.0,
    ) -> Union[Dict, str, bytes]:
        """
        Выполняет HTTP запрос.

        Args:
            method: HTTP метод (GET, POST, PUT, PATCH, DELETE).
            endpoint: Путь к API endpoint.
            host: Хост для запроса (переопределяет дефолтный).
            data: Данные form-data.
            body_payload: JSON тело запроса.
            header_payload: Дополнительные заголовки.
            url_payload: Query параметры.
            files: Файлы для multipart/form-data загрузки.
            expected_response_code: Ожидаемый HTTP статус код.
            timeout: Максимальное время ожидания ответа в секундах.
            allow_redirects: Автоматически следовать HTTP редиректам.
            is_binary: Возвращает response.content (bytes).
            return_cookies: Возвращает куки вместо JSON.
            attempts: Количество попыток при любом исключении.
            retry_delay: Пауза в секундах между попытками.

        Returns:
            Dict — если сервер вернул валидный JSON.
            str  — если сервер вернул текст.
            bytes — если is_binary=True.

        Raises:
            AssertionError: Статус код не совпал с expected_response_code.
            requests.Timeout: Сервер не ответил за timeout секунд.
            Exception: Последнее исключение если все attempts исчерпаны.
        """

        url = (host or self._host) + endpoint
        headers = self._prepare_headers(files, body_payload, data, header_payload)
        last_exception: Optional[Exception] = None

        for attempt in range(1, attempts + 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    params=url_payload,
                    data=data,
                    json=body_payload,
                    files=files,
                    headers=headers,
                    timeout=timeout,
                    verify=False,
                    allow_redirects=allow_redirects,
                )

                assert response.status_code == expected_response_code, (
                    f"Ожидался статус {expected_response_code}, "
                    f"получен {response.status_code}. "
                    f"URL: {url}, Body: {response.text}"
                )

                request_logger.log_info(response)

                if is_binary:
                    return response.content

                if return_cookies:
                    return dict(response.cookies)

                try:
                    return response.json()
                except JSONDecodeError:
                    return response.text

            except Exception as e:
                last_exception = e
                if attempt < attempts:
                    time.sleep(retry_delay)

        raise last_exception

    def _prepare_headers(
        self,
        files: Optional[Dict],
        body_payload: Optional[Dict],
        data: Optional[Union[Dict, str]],
        header_payload: Optional[Dict[str, str]],
    ) -> Dict[str, str]:
        """Подготавливает заголовки для запроса."""
        headers = self._headers.copy()

        if files:
            headers.pop("Content-Type", None)
        elif body_payload is not None:
            headers.setdefault("Content-Type", "application/json")
        elif data:
            headers.setdefault("Content-Type", "application/x-www-form-urlencoded")

        if header_payload:
            headers.update(header_payload)

        return headers

    def get(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполняет GET запрос."""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполняет POST запрос."""
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполняет PUT запрос."""
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполняет PATCH запрос."""
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполняет DELETE запрос."""
        return self._request("DELETE", endpoint, **kwargs)

    def get_binary(self, endpoint: str, **kwargs) -> bytes:
        """Выполняет GET запрос для бинарных данных."""
        return self._request("GET", endpoint, is_binary=True, **kwargs)

    def post_binary(self, endpoint: str, **kwargs) -> bytes:
        """Выполняет POST запрос для бинарных данных."""
        return self._request("POST", endpoint, is_binary=True, **kwargs)