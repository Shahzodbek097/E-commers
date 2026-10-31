from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from rest_framework import serializers, generics

from products.models import Product, Chegirma, ProductViewHistory

class ChegirmaListCreateView(generics.ListCreateAPIView):
    queryset = Chegirma.objects.all()

    class ChegirmSerializer(serializers.ModelSerializer):
        class Meta:
            model=Chegirma
            fields='__all__'

    serializer_class=ChegirmSerializer


@api_view(['GET'])
def chegirmada(request, product_id):
    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Bunday Mahsulot yoq'}, status=status.HTTP_404_NOT_FOUND)

    user_viewed=ProductViewHistory.objects.filter(user=request.user, product=product).exists()
    yaqin_chegirma=Chegirma.objects.filter(product=product, boshlanishi__lte=timezone.now() + timedelta(hours=24)).first()

    if user_viewed and yaqin_chegirma:
        foizi=yaqin_chegirma.chegirma_foizi
        boshlanish_vaqti=yaqin_chegirma.boshlanishi
        tugash_vaqti=yaqin_chegirma.tugashi
        return Response({
            'xabar': f"Bu mahsulotga hozirda {foizi} % chegirma e'lon qilingan",
            'boshlanishi': boshlanish_vaqti,
            'tugashi': tugash_vaqti
        })
    else:
        return Response({
            'xabar': "Bu mahsulotga vaqtincha chegirma yo'q."
        })