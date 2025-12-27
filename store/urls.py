from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-paypal-payment/', views.process_paypal_payment, name='process_paypal_payment'),
    path('process-card-payment/', views.process_card_payment, name='process_card_payment'),
    path('order-success/', views.order_success, name='order_success'),
    path('profile/', views.profile, name='profile'),
    path('order-history/', views.order_history, name='order_history'),
]