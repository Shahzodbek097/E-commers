from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from products.models import Product


@api_view(['POST'])
@swagger_auto_schema(operation_description='Admin')
@staff_member_required
def admin_qoshish_ombor(requests, product_id, zakas_soni):
    try:
        product=Product.objects.get(id=product_id)
        product.qoshish_ombor(zakas_soni)
        return JsonResponse({'status': 'succes', 'message': f"ombor by {zakas_soni}"})

    except Product.DoesNotExits:
        return JsonResponse({'status': 'error', 'message': 'Product mavjud emas'}, status=400)

    except ValueError:
        return HttpResponseBadRequest('Invalid input.')

