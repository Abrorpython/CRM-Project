from django.urls import path

from .views import SearchProductCategory, SearchProduct, StatusProduct

urlpatterns = [
    path('searchcategory/<int:pk>/', SearchProductCategory.as_view({'get': 'list'})),
    path('', SearchProduct.as_view()),
    path('status/', StatusProduct.as_view({'get': 'list'})),
]