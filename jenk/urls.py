"""
URL configuration for jenk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from api import views
from website import views as website_views
from Loan import views as loan_views
from api.views import BankApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', views.BankApiView.as_view(), name="BankApiViews"),
    path('api/', include('api.urls')),
    path('', website_views.index, name="index"),
    path('about/', website_views.about, name="about"),
    path('login/', website_views.login, name="login"),
    path('register/', website_views.register, name="register"),
    path('logout/', website_views.logout, name="logout"),
    # define post method url
    # path('api/post/', views.BankApiView.as_view(), name="BankApiPostViews"),

    path('loans/', loan_views.view_loans, name="view_loans"),
    path('loan-dashboard/', loan_views.loan_dashboard, name="loan_dashboard"),

    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/dashboard/', BankApiView.as_view()),
]