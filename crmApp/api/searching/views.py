from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from crmApp.models import Product
from crmApp.api.products.serializers import ProductSerializers


# for status
class StatusProduct(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def list(self, request, *args, **kwargs):
        product = Product.objects.filter(amount__lte=5)
        serializers = ProductSerializers(product, many=True)
        return Response({
            "ok": serializers.data
        })


# Mahsulotni qidirish nomi bo'yicha
class SearchProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['^name']


# Categoriya bo'yicha qidiruv
class SearchProductCategory(ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = Product.objects.filter(category_id=kwargs['pk'])
        serializers = ProductSerializers(queryset, many=True)
        return Response({"success": True,
                         "data": serializers.data,
                         "message": f"{status.HTTP_200_OK}"
                         })
