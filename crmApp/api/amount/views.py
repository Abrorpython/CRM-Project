from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from crmApp.models import Product, AgentSalesProduct
from crmApp.api.products.serializers import AgentSalesProductSerializer

@api_view(['GET'])
def amountProduct(request):
    if request.method == 'GET':
        products = Product.objects.all()
        agentSales = AgentSalesProduct.objects.all()
        amount = 0
        sales = 0
        foyda = 0
        sotildi = 0

        for i in agentSales:
            sotildi = sotildi + i.quantity

        for i in products:
            amount = amount + i.amount
            sales = sales + (i.sel_price) * (i.amount)
            foyda = foyda + (i.finish_price) * (i.amount)
        return Response({"success": True,
                        "jami_mahsulotlar": amount,
                         "sotilgan_jami_mahsulotlar": sotildi,
                         'olindi_jami_mahsulotlar_yigindisi': sales,
                         'sotildi_jami_jami_mahsulotlar_yigindisi': foyda,
                         'jami_foyda': foyda-sales,
                        "message": f"{status.HTTP_200_OK}"
                         })
    else:
        return Response({
            "success": "hatolik",
            "message": f"{status.HTTP_404_NOT_FOUND}"
        })


class AgentSalesProductTotal(ModelViewSet):
    serializer_class = AgentSalesProductSerializer
    queryset = AgentSalesProduct

    def list(self, request, *args, **kwargs):
        user = request.user
        order = AgentSalesProduct.objects.all().filter(user=user)
        serializers = AgentSalesProductSerializer(order, many=True)
        return Response(serializers.data)