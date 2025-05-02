from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products', views.product_list, name = 'product_list'),
    path('cart', views.cart, name = 'cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('graphs', views.graphs, name = 'graphs')
    ]