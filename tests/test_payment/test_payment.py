import pytest
import pytest_check as check


@pytest.mark.payments
def test_create_payment(qiwi, user_data):
    """Создание платежа на 1 рубль."""
    payment = qiwi.payments.create_payment(to_wallet=qiwi.user_data.wallet, amount=1.0)
    check.is_not_none(payment.transaction.id, "transaction.id отсутствует")
    check.equal(payment.transaction.state.code, "Accepted",
                f"Ожидался Accepted, получен {payment.transaction.state.code}")


@pytest.mark.payments
def test_execute_payment(qiwi, user_data):
    """Исполнение созданного платежа."""
    payment = qiwi.payments.create_payment(to_wallet=qiwi.user_data.wallet, amount=1.0)
    transaction = qiwi.payments.get_transaction(txn_id=payment.transaction.id)
    assert transaction.status == "SUCCESS", f"Ожидался SUCCESS, получен {transaction.status}"
