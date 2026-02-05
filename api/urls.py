from django.urls import path
from .views import BankApiView
from .views import APILoginView, ProfileAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', APILoginView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileAPI.as_view(), name='profile_api'),
]