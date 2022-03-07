from django.urls import path

from .views import RegistrationView, \
                    LoginAPIView, UserListView, AgentSalesProductAmount

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user-list/', UserListView.as_view({'get': 'list'}), name='user-list'),
    path('user-list/<int:pk>/', UserListView.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='user-retrive'),
    path('hisob-kitob/<int:user_id>/', AgentSalesProductAmount.as_view())
]