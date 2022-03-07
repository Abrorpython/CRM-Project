from django.urls import path

from .views import CategoryView, ProductView, ScannerQrKod,\
    ProductUpdateAmountView, AgentBasketProductViews, AgentSalesProductViews

urlpatterns = [
    path('category/', CategoryView.as_view({'get': 'list', 'post': 'create'})),
    path('category/<int:pk>/', CategoryView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('product/', ProductView.as_view({'get': 'list', 'post': 'create'})),
    path('product/<int:pk>/', ProductView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('scanner/<int:qr>/', ScannerQrKod.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('product/amount/<int:product_id>/', ProductUpdateAmountView.as_view(), name='update-amount'),
    path('basket/<int:pk>/', AgentBasketProductViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('basket/', AgentBasketProductViews.as_view({'get': 'list', 'post': 'create'}), name='agent-sales-detail'),
    path('sales/', AgentSalesProductViews.as_view({'get': 'list'})),
    path('sales/<int:pk>/', AgentSalesProductViews.as_view({'get': 'retrieve'})),
]