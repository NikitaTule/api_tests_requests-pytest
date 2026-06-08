import logging
import os

import pytest

from services.qiwi.qiwi_service import QiwiService
from utils.config_reader import app_config

logging.getLogger("urllib3").setLevel(logging.WARNING)


@pytest.fixture(scope="class")
def user_data():
    """Данные тестового пользователя из users.yaml."""
    return app_config.users.qiwi_user


@pytest.fixture(scope="class")
def qiwi(user_data) -> QiwiService:
    """Фикстура сервиса QIWI."""
    return QiwiService(
        user_data=user_data,
        headers={"Authorization": f"Bearer {os.getenv('QIWI_TOKEN')}"},
    )
