from django.urls import path
from .views import BankApiView

urlpatterns = [
    path('post/', BankApiView.as_view()),
    path('get/', BankApiView.as_view()),
]