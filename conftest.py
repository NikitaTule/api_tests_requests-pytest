import logging
import os

import pytest

from services.qiwi.qiwi_service import QiwiService
from utils.config_reader import app_config

logging.getLogger("urllib3").setLevel(logging.WARNING)


@pytest.fixture(scope="class")
def user_data(request):
    """
    Данные тестового пользователя из users.yaml.
    Поддерживает выбор пользователя через маркер @pytest.mark.user("user_name").
    По умолчанию используется qiwi_user.
    """
    user_marker = request.node.get_closest_marker("user")
    if user_marker is None:
        return app_config.users.qiwi_user
    user_name = user_marker.args[0]
    return app_config.users[user_name]


@pytest.fixture(scope="class")
def qiwi(user_data):
    """Фикстура сервиса QIWI."""
    return QiwiService(
        user_data=user_data,
        headers={"Authorization": f"Bearer {user_data.token}"},
    )