from rest_framework import serializers

from crmApp.models import Income, Expense


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'income', 'descriptions', 'data']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'expense', 'descriptions', 'data']