from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from products.serializers import *
from products.models import *
from products.permissions import IsOwnerOrReadOnly



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsOwnerOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class BahoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Baho.objects.all()
    serializer_class = BahoSerializers