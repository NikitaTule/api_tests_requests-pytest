import pytest
import pytest_check as check


@pytest.mark.smoke
def test_get_balance(qiwi):
    """Баланс кошелька возвращает валидную структуру ответа."""
    qiwi.balance.get_balance()


@pytest.mark.balance
def test_balance_is_positive(qiwi):
    """Баланс кошелька в рублях должен быть больше 0."""
    balance = qiwi.balance.get_balance()
    rub_account = next((a for a in balance.accounts if a.currency == 643), None)
    check.is_not_none(rub_account, "Рублёвый счёт не найден")
    check.greater(rub_account.balance.amount, 0,
                  f"Баланс должен быть больше 0, получен {rub_account.balance.amount}")
