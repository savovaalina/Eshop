"""
URL configuration for Eshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from EshopJewerly import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profiles/', views.user_profiles, name='user_profiles'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('order_confirmation_modal/<int:order_id>/', views.order_confirmation_modal, name='order_confirmation_modal'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('bought_products/', views.bought_products, name='bought_products'),
    path('update_quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('category/<int:category_id>/edit/', views.edit_product, name='edit_product'),
    path('', views.product_list, name='product_list'),
    path('orders/', views.orders_list, name='orders_list'),
    path('', views.product_list, name='home'),
    path('place_order_multiple/', views.place_order_multiple, name='place_order_multiple'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_manufacturer/', views.add_manufacturer, name='add_manufacturer'),
    path('add_product/', views.add_product, name='add_product'),
    path('categories/', views.category_list, name='category_list'),
    path('manufacturer_list/', views.manufacturer_list, name='manufacturer_list'),
    path('edit_manufacturer/<int:manufacturer_id>/', views.edit_manufacturer, name='edit_manufacturer'),
    path('delete_manufacturer/<int:manufacturer_id>/', views.delete_manufacturer, name='delete_manufacturer'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
