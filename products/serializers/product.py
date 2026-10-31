from rest_framework import serializers
from products.models import *

class ProductSerializers(serializers.ModelSerializer):
    orta_reyting=serializers.FloatField(read_only=True, required=False)

    class Meta:
        model=Product
        fields=['id', 'nomi', 'narxi', 'izoh', 'category', 'ombor', 'orta_reyting']


class ProductHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductViewHistory
        fields='__all__'