from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [


    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profiles/', views.user_profiles, name='user_profiles'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('order_confirmation_modal/<int:order_id>/', views.order_confirmation_modal, name='order_confirmation_modal'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('bought_products/', views.bought_products, name='bought_products'),
    path('update_quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('', views.product_list, name='home'),
    path('/products', views.product_list, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
path('category_list/', views.category_list, name='category_list'),  # Example URL pattern for category list
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)