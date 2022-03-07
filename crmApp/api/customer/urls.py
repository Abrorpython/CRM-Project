from django.urls import path

from . import views

urlpatterns = [
    path('create-customer/', views.CreateCustomListView.as_view(), name='create-custom'),
    path('create-customer/<int:customer_id>/', views.CustomDetailView.as_view(), name='detail-customer'),
    path('customer-list/', views.CustomListView.as_view(), name='customers-list')
]