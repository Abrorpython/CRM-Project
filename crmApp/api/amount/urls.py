from django.urls import path

from . import views


urlpatterns = [
    path('amount-products/', views.amountProduct, name='amount'),
    path('order/', views.AgentSalesProductTotal.as_view({'get': 'list', 'post': 'create'}), name='order')
]