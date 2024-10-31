from rest_framework import serializers


class WalletOperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=["DEPOSIT", "WITHDRAW"])
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
