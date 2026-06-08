import pytest


@pytest.mark.smoke
def test_get_profile(qiwi):
    """Профиль пользователя возвращает валидную структуру ответа."""
    qiwi.profile.get_profile()
