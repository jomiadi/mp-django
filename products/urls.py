# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/order/<str:order_type>/', views.create_order, name='create_order'),
    path('active_orders/', views.active_orders, name='active_orders'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
]
