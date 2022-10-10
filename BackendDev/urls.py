"""BackendDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from BackendDev import views as main_views
from data import views as data_views
from rest_framework import routers
from views import HIEViewSet

router = routers.DefaultRouter()
router.register(r'HIEs', HIEViewSet)

urlpatterns = [
    path('admin/', admin.site.urls), #access: localhost:8000/admin/
    path('', main_views.index, name='index'), #access: localhost:8000/
    path('files/', main_views.files, name='files'), #access: localhost:8000/files/
    path('api/', data_views.api, name='api') #access: localhost:8000/api/
    
]
