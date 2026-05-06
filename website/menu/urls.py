from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'menu'

urlpatterns = [
    path('', views.index, name='index'),
    path('place_order/<int:item_id>/', views.place_order, name='place_order'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('review/<int:item_id>/', views.add_review, name='add_review'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.payment_qr, name='payment_qr'),
]


