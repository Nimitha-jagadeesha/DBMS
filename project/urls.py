"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from ForestManagement import views
# from . import rango
urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.list_products, name='listitems'),
    path('list_orders_staff', views.list_orders, name='list_orders_staff'),
    path('list_orders/<str:username>', views.UserOrderListView.as_view(), name='list_orders'),
    path('add_items/', views.add_products, name='add_items'),
    path('place_order/', views.OrderCreateView.as_view(), name='place_order'),
    path('admin/', admin.site.urls),
    path('update_products/<str:pk>/', views.update_products, name="update_items"),
    path('delete_products/<str:pk>/', views.delete_products, name="delete_products"),
    path('accounts/', include('registration.backends.default.urls')),
]
