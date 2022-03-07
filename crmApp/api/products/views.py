from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import CategorySerializers, ProductSerializers, \
    AgentSalesProductSerializer, ProductAmountUpdateSerializer

from crmApp.models import Category, Product, AgentSalesProduct


class AgentSalesProductViews(ModelViewSet):
    queryset = AgentSalesProduct.objects.all()
    serializer_class = AgentSalesProductSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        products = AgentSalesProduct.objects.filter(user=user, status=True)
        serializer = AgentSalesProductSerializer(products, many=True)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        sales = get_object_or_404(AgentSalesProduct, pk=kwargs['pk'], user=user, status=True)
        product = AgentSalesProduct.objects.get(pk=kwargs['pk'])
        sum1 = (float(product.quantity) * float(product.product.finish_price))
        sum2 = (float(product.quantity) * float(product.product.sel_price))
        sum3 = sum1 - sum2
        serializer = AgentSalesProductSerializer(sales)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "agent": {
                                "jami": sum1,
                                "foyda": sum3,
                                },
                            "message": f"{status.HTTP_201_CREATED}"
                        })


# har bir Agent savatchaga qo`shgan mahsulotini o`zgartira olishi va o`qib olishi faqat o`zi qo`shgan
class AgentBasketProductViews(ModelViewSet):
    queryset = AgentSalesProduct.objects.all()
    serializer_class = AgentSalesProductSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        products = AgentSalesProduct.objects.filter(user=user, status=False)
        serializer = AgentSalesProductSerializer(products, many=True)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}",
                        })

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        new_sales = AgentSalesProduct.objects.create(
            product=Product.objects.get(id=data['product']),
            user=user,
            quantity=data['quantity'],
            data=data['data']
        )
        new_sales.save()
        sum1 = (float(new_sales.quantity) * float(new_sales.product.finish_price))
        sum2 = (float(new_sales.quantity) * float(new_sales.product.sel_price))
        sum3 = sum1 - sum2
        serializer = AgentSalesProductSerializer(new_sales)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "agent": {
                                "jami": sum1,
                                "foyda": sum3,
                                },
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        sales = get_object_or_404(AgentSalesProduct, pk=kwargs['pk'], user=user, status=False)
        product = AgentSalesProduct.objects.get(pk=kwargs['pk'])
        sum1 = float(product.quantity) * float(product.product.finish_price)
        sum2 = float(product.quantity) * float(product.product.sel_price)
        sum3 = sum1 - sum2
        serializer = AgentSalesProductSerializer(sales)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "agent": {
                                "jami": sum1,
                                "foyda": sum3,
                                },
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def update(self, request, *args, **kwargs):
        sales = self.get_object()
        data = request.data
        product = Product.objects.get(id=data['product'])
        sales.product = product
        sales.quantity = data['quantity']
        sales.data = data['data']
        sales.status = data['status']
        sales.save()
        product = AgentSalesProduct.objects.get(pk=kwargs['pk'])
        sum1 = float(product.quantity) * float(product.product.finish_price)
        sum2 = float(product.quantity) * float(product.product.sel_price)
        sum3 = sum1 - sum2
        serializer = AgentSalesProductSerializer(sales)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "agent": {
                                "jami": sum1,
                                "foyda": sum3,
                                },
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def destroy(self, request, *args, **kwargs):
        user = request.user
        agentsales = get_object_or_404(AgentSalesProduct, pk=kwargs['pk'], user=user, status=False)
        agentsales.delete()
        return Response({"success": True,
                         "message": f"{status.HTTP_204_NO_CONTENT}"
                         })


# Har bir sotilgan mahsulotni
class ProductUpdateAmountView(generics.GenericAPIView):
    serializer_class = ProductAmountUpdateSerializer

    def put(self, request, product_id):
        amount = get_object_or_404(Product, pk=product_id)
        data = request.data
        serializer = self.serializer_class(data=data, instance=amount)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}"
                            })
        else:
            return Response({
                "success": serializer.errors,
                "message": f"{status.HTTP_404_NOT_FOUND}"
            })


# Scanner QR kod
class ScannerQrKod(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def retrieve(self, request, *args, **kwargs):
        product = Product.objects.get(qr=kwargs['qr'])
        serializer = ProductSerializers(product)
        return Response({"success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def update(self, request, *args, **kwargs):
        product = Product.objects.get(qr=kwargs['qr'])
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,
                             "data": serializer.data,
                             "message": f"{status.HTTP_201_CREATED}"
                             })
        else:
            return Response({
                "success": serializer.errors,
                "message": f"{status.HTTP_404_NOT_FOUND}"
            })

    def destroy(self, request, *args, **kwargs):
        product = Product.objects.get(qr=kwargs['qr'])
        product.delete()
        return Response({"success": True,
                         "message": f"{status.HTTP_204_NO_CONTENT}"
                         })


# for Product
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializers = ProductSerializers(products, many=True)
        return Response({"success": True,
                         "data": serializers.data,
                         "message": f"{status.HTTP_200_OK}"
                         })

    def create(self, request, *args, **kwargs):
        data = request.data
        new_product = Product.objects.create(category=Category.objects.get(id=data['category']),
                                             name=data['name'],
                                             amount=data['amount'],
                                             parametr=data['parametr'],
                                             image=data['image'],
                                             qr=data['qr'],
                                             sel_price=data['sel_price'],
                                             finish_price=data['finish_price'],
                                             date=data['date'],
                                             descriptions=data['descriptions'])
        new_product.save()
        serializer = ProductSerializers(new_product)
        return Response({
                            "success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_200_OK}"
                            })

    def retrieve(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        serializer = ProductSerializers(product)
        return Response({"success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        data = request.data

        category = Category.objects.get(id=data['category'])

        product.category = category
        product.name = data['name']
        product.amount = data['amount']
        product.parametr = data['parametr']
        product.image = data['image']
        product.qr = data['qr']
        product.sel_price = data['sel_price']
        product.finish_price = data['finish_price']
        product.date = data['date']
        product.descriptions = data['descriptions']
        product.save()
        serializer = ProductSerializers(product)
        return Response({
                        "success": True,
                        "data": serializer.data,
                        "message": f"{status.HTTP_201_CREATED}"
                        })


    def destroy(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        product.delete()
        return Response({"success": True,
                        "message": f"{status.HTTP_204_NO_CONTENT}"
                         })

    def partial_update(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        serializer = ProductSerializers(product, data=request.data, partial=True)
        serializer.save()
        serializer.is_valid(raise_exception=True)
        return Response({"ok": serializer.data})


# For category
class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def list(self, request, *args, **kwargs):
        categorys = Category.objects.all()
        serializers = CategorySerializers(categorys, many=True)
        return Response({"success": True,
                         "data": serializers.data,
                         "message": f"{status.HTTP_200_OK}"
                         })

    def create(self, request, *args, **kwargs):
        serializers = CategorySerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({
                            "success": True,
                            "data": serializers.data,
                            "message": f"{status.HTTP_200_OK}"
                            })
        else:
            return Response({
            "success": serializers.errors,
            "message": f"{status.HTTP_404_NOT_FOUND}"
            })

    def retrieve(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        serializer = CategorySerializers(category)
        return Response({"success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}"
                        })

    def update(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        serializer = CategorySerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,
                            "data": serializer.data,
                            "message": f"{status.HTTP_201_CREATED}"
                            })
        else:
            return Response({
            "success": False,
            "message": f"{status.HTTP_404_NOT_FOUND}"
        })

    def destroy(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        category.delete()
        return Response({"success": True,
                        "message": f"{status.HTTP_204_NO_CONTENT}"
                         })
