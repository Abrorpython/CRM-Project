from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateCustomSerializers, CustomDetailSerializer, CustomListSerializer
from crmApp.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomListView(generics.GenericAPIView):
    serializer_class = CustomListSerializer
    queryset = Customer

    def get(self, request):
        customers = Customer.objects.all()
        serializers = self.serializer_class(instance=customers, many=True)
        return Response({
                         "success": True,
                         "data": serializers.data,
                         "message": f"{status.HTTP_200_OK}"
            })


# Mijoz qo`shish
class CreateCustomListView(generics.GenericAPIView):
    serializer_class = CreateCustomSerializers
    queryset = Customer.objects.all()

    def get(self, request):
        user = request.user
        customer = Customer.objects.filter(user=user)
        serializer = self.serializer_class(instance=customer, many=True)
        return Response({
                         "success": True,
                         "data": serializer.data,
                         "message": f"{status.HTTP_200_OK}"
            })

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({
                            "success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_200_OK}"
                })
        else:
            return Response({
                    "success": serializer.errors,
                    "message": f"{status.HTTP_404_NOT_FOUND}"
            })


# Har bir agent qo`shgan bir dona Mijozni o`chirish, o`zgartirish, bir donasini o`qib olish
class CustomDetailView(generics.GenericAPIView):
    serializer_class = CustomDetailSerializer

    def get(self, request, customer_id):
        user=request.user
        customer = get_object_or_404(Customer, pk=customer_id, user=user)
        serializer = self.serializer_class(instance=customer)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_200_OK}"
                })

    def put(self, request, customer_id):
        user = request.user
        data = request.data
        customer = get_object_or_404(Customer, pk=customer_id, user=user)
        serializer = self.serializer_class(data=data, instance=customer)
        if serializer.is_valid():
            serializer.save()
            return Response({
                            "success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_200_OK}"
                })
        else:
            return Response({
                    "success": serializer.errors,
                    "message": f"{status.HTTP_404_NOT_FOUND}"
            })

    def delete(self, request, customer_id):
        user = request.user
        customer = get_object_or_404(Customer, pk=customer_id, user=user)
        customer.delete()
        return Response({
                    "message": f"{status.HTTP_404_NOT_FOUND}"
            })