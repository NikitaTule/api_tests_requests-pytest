"""
Модуль логирования HTTP запросов.
"""

import logging

import requests


logger = logging.getLogger(__name__)


class RequestLogger:
    """Логгер HTTP запросов и ответов."""

    def log_info(self, response: requests.Response) -> None:
        """Логирует метод, URL и статус код."""
        logger.info(
            f"\n  ➤ {response.request.method} {response.request.url}"
            f"\n  ✔ {response.status_code} {response.url}"
        )

    def log_debug(self, response: requests.Response) -> None:
        """Логирует полные детали запроса и ответа."""
        body = response.request.body or "—"
        cookies = dict(response.cookies) or "—"

        logger.debug(
            f"\n  Request Headers : {dict(response.request.headers)}"
            f"\n  Request Body    : {body}"
            f"\n  Response Status : {response.status_code}"
            f"\n  Response Body   : {response.text[:500]}"
            f"\n  Cookies         : {cookies}"
        )


request_logger = RequestLogger()