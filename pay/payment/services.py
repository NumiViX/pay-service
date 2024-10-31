from django.db import transaction
from .models import Wallet


class WalletService:
    @staticmethod
    @transaction.atomic
    def deposit(wallet_id, amount):
        wallet = Wallet.objects.select_for_update().get(id=wallet_id)
        wallet.balance += amount
        wallet.save()
        return wallet.balance

    @staticmethod
    @transaction.atomic
    def withdraw(wallet_id, amount):
        wallet = Wallet.objects.select_for_update().get(id=wallet_id)
        if wallet.balance < amount:
            raise ValueError("Insufficient funds")
        wallet.balance -= amount
        wallet.save()
        return wallet.balance

    @staticmethod
    def perform_operation(wallet_id, operation_type, amount):
        operations = {
            "DEPOSIT": WalletService.deposit,
            "WITHDRAW": WalletService.withdraw
        }
        if operation_type not in operations:
            raise ValueError("Invalid operation type")
        return operations[operation_type](wallet_id, amount)
