from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as django_filters

from products.filter import ProductFilter
from products.permissions import IsStaffOrReadOnly
from products.serializers import *
from products.models import *


class CustomPagination(PageNumberPagination):
    page_size = 3


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    pagination_class = CustomPagination

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class=ProductFilter
    search_fields=['nomi', 'izoh']


    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products=Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializer=ProductSerializers(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
        })

    @action(detail=False, methods=['get'])
    def yuqori_reyting(self, request):
        top_product=Product.objects.annotate(orta_reyting=models.Avg('baho__reyting')).order_by('-orta_reyting')[:2]
        serializer=ProductSerializers(top_product, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def ortacha_reyting(self, request, pk=None):
        product=self.get_object()
        baho=product.baho.all()

        if baho.count()==0:
            return Response({'orta_baho':'Baholar yoq'})

        orta_reyting=sum([bahosi.reyting for bahosi in baho]) / baho.count()

        return Response({'ortacha_reyting': orta_reyting})