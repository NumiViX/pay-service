import pytest
from payment.models import Wallet
from payment.services import WalletService


@pytest.fixture
def wallet(db):
    # Создаем тестовый кошелек с начальными данными
    return Wallet.objects.create(balance=1000)


@pytest.mark.django_db
class TestWalletService:
    def test_deposit(self, wallet):
        # Проверяем успешное пополнение баланса
        new_balance = WalletService.deposit(wallet.id, 500)
        wallet.refresh_from_db()
        assert wallet.balance == 1500
        assert new_balance == 1500

    def test_withdraw_successful(self, wallet):
        # Проверяем успешное снятие средств
        new_balance = WalletService.withdraw(wallet.id, 500)
        wallet.refresh_from_db()
        assert wallet.balance == 500
        assert new_balance == 500

    def test_withdraw_insufficient_funds(self, wallet):
        # Проверяем случай недостатка средств
        with pytest.raises(ValueError, match="Insufficient funds"):
            WalletService.withdraw(wallet.id, 2000)
        wallet.refresh_from_db()
        assert wallet.balance == 1000  # Баланс не должен измениться

    def test_perform_operation_deposit(self, wallet):
        # Проверка работы perform_operation с операцией DEPOSIT
        new_balance = WalletService.perform_operation(wallet.id, "DEPOSIT", 500)
        wallet.refresh_from_db()
        assert wallet.balance == 1500
        assert new_balance == 1500

    def test_perform_operation_withdraw(self, wallet):
        # Проверка работы perform_operation с операцией WITHDRAW
        new_balance = WalletService.perform_operation(wallet.id, "WITHDRAW", 500)
        wallet.refresh_from_db()
        assert wallet.balance == 500
        assert new_balance == 500

    def test_perform_operation_invalid_operation(self, wallet):
        # Проверка некорректного типа операции
        with pytest.raises(ValueError, match="Invalid operation type"):
            WalletService.perform_operation(wallet.id, "TRANSFER", 500)
        wallet.refresh_from_db()
        assert wallet.balance == 1000  # Баланс не должен измениться
