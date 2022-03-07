from django.urls import path, include


urlpatterns = [
    path('v1/', include('crmApp.api.users.urls')),
    path('v1/', include('crmApp.api.products.urls')),
    path('v1/', include('crmApp.api.kassa.urls')),
    path('v1/', include('crmApp.api.searching.urls')),
    path('v1/', include('crmApp.api.amount.urls')),
    path('v1/', include('crmApp.api.customer.urls')),
]