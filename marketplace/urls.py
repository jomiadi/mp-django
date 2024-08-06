# marketplace/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from products import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.home, name='home'),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('filter_products/', product_views.filter_products, name='filter_products'),  # Новый маршрут
]
