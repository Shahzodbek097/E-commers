from rest_framework import serializers
from products.models import *


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class BahoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Baho
        fields='__all__'