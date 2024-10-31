from django.urls import path
from .views import WalletOperationView as WOP, WalletBalanceView as WBV

urlpatterns = [
    path('wallets/<uuid:wallet_id>/operation', WOP.as_view(), name='wallet_operation'),
    path('wallets/<uuid:wallet_id>', WBV.as_view(), name='wallet_balance'),
]
