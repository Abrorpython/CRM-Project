from django.urls import path

from .views import IncomeView, ExpenseView
from .views import listIncome, listExpense, income_expense

urlpatterns = [
    path('incomes/', IncomeView.as_view({'get': 'list', 'post': 'create'})),
    path('income-list/<int:pk>/', IncomeView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('income-list/', listIncome),
    path('expences/', ExpenseView.as_view({'get': 'list', 'post': 'create'})),
    path('expence-list/<int:pk>/', ExpenseView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('expence-list/', listExpense, name='chiqimlar_listi'),
    path('income-expence/<str:start>-<str:finish>/', income_expense, name='chart')
]