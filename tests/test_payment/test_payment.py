import pytest
import pytest_check as check


@pytest.mark.smoke
@pytest.mark.payments
def test_create_payment(qiwi, user_data):
    """Создание платежа на 1 рубль."""
    payment = qiwi.payments.create_payment(to_wallet=qiwi.user_data.wallet, amount=1.0)
    check.is_not_none(payment.transaction.id, "transaction.id отсутствует")
    check.equal(payment.transaction.state.code, "Accepted",
                f"Ожидался Accepted, получен {payment.transaction.state.code}")


@pytest.mark.smoke
@pytest.mark.payments
def test_execute_payment(qiwi, user_data):
    """Исполнение созданного платежа."""
    balance_before = qiwi.balance.get_balance()
    rub_before = next((a for a in balance_before.accounts if a.currency == 643), None)

    payment = qiwi.payments.create_payment(to_wallet=user_data.wallet, amount=1.0)
    transaction = qiwi.payments.get_transaction(txn_id=payment.transaction.id)

    balance_after = qiwi.balance.get_balance()
    rub_after = next((a for a in balance_after.accounts if a.currency == 643), None)

    check.equal(transaction.status, "SUCCESS", f"Ожидался SUCCESS, получен {transaction.status}")
    check.less(rub_after.balance.amount, rub_before.balance.amount, "Баланс не изменился после платежа")
