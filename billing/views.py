from rest_framework import views, status, request
from rest_framework.response import Response
from django.conf import settings
import stripe
from .models import Payment
from products.models import Order
# from billing.serializers import PaymentSerializers

stripe.api_key = settings.STRIPE_SECRET_KEY


class TolovView(views.APIView):
    # serializer_class=PaymentSerializers

    def post(self, requests, *args, **kwargs):
        klent_token=request.data.get('klent_token')
        order_id=request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Bunaqa zakas yo'q"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            umum_hisob=order.product.narxi * order.nechta
            chiqim=stripe.Charge.create(
                qancha=int(umum_hisob * 100),
                pul_birligi='usd',
                kimdan=klent_token,
            )

            Payment.objects.create(
                order=order,
                chiqim_id=chiqim['id'],
                qancha=umum_hisob
            )

            order.is_paid=True
            order.save()

            return Response({'status': "To'lov qabul qilindi"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

