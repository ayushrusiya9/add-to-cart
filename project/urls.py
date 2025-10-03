from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.product_list, name='product_list'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:product_id>/',views.remove_item,name='remove'),
    path('payment/',views.payment,name='payment'),
    path('payment-status/',views.payment_status,name='payment-status')
]