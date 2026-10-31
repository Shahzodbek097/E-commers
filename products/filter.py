from django_filters import rest_framework as django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_narx=django_filters.NumberFilter(field_name='narxi', lookup_expr='gte')
    max_narx=django_filters.NumberFilter(field_name='narxi', lookup_expr='lte')

    class Meta:
        model=Product
        fields=['category', 'min_narx', 'max_narx']
