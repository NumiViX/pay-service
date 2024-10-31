from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payment.models import Wallet
from payment.services import WalletService
from .serializers import WalletOperationSerializer


class WalletOperationView(APIView):
    def post(self, request, wallet_id):
        serializer = WalletOperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        operation_type = serializer.validated_data['operationType']
        amount = serializer.validated_data['amount']

        try:
            balance = WalletService.perform_operation(
                wallet_id,
                operation_type,
                amount)
            return Response(
                {"balance": balance},
                status=status.HTTP_200_OK)

        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WalletBalanceView(APIView):
    def get(self, request, wallet_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id)
            return Response(
                {"balance": wallet.balance},
                status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_404_NOT_FOUND)
