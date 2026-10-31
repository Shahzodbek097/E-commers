from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from products.serializers import ProductHistorySerializer
from products.models import ProductViewHistory

class ProductViewHistoryCreate(APIView):
    serializer_class=ProductHistorySerializer

    @swagger_auto_schema(request_body=ProductHistorySerializer)
    def post(self, request):
        serializer=ProductHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ProductHistory_list(request):
    producthistory=ProductViewHistory.objects.all()
    serializer=ProductHistorySerializer(producthistory, many=True)
    return Response(serializer.data)



