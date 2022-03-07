from rest_framework import serializers
from django.db.models import Q

from crmApp.models import Category, Product, AgentSalesProduct


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'date']

    def validate_name(self, value):
        name_query = Category.objects.filter(name=value)
        if name_query.exists():
            raise serializers.ValidationError("Ushbu bo'lim oldin mavjud")
        return value


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'amount', 'parametr', 'image', 'qr', 'sel_price',
                  'finish_price', 'date', 'descriptions']
        depth = 1

    def validate_name(self, value):
        name_query = Product.objects.filter(name=value)
        if name_query.exists():
            raise serializers.ValidationError('Ushbu mahsulot oldin mavjud')
        return value



class AgentSalesProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentSalesProduct
        fields = ['id', 'product', 'quantity', 'data', 'status']
        depth = 2


class ProductAmountUpdateSerializer(serializers.ModelSerializer):

    amount = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['amount']

