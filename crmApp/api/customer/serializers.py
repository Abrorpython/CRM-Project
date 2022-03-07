from rest_framework import serializers

from crmApp.models import Customer


class CreateCustomSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    number = serializers.CharField(max_length=32)
    descriptions = serializers.CharField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'number', 'descriptions']


class CustomDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    number = serializers.CharField(max_length=32)
    descriptions = serializers.CharField()
    create_at = serializers.DateTimeField()
    update_at = serializers.DateTimeField()

    class Meta:
        model = Customer
        fields = ['id', 'name', 'number', 'descriptions', 'create_at', 'update_at']


class CustomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        depth = 1


