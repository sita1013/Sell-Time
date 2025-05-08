from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('products', views.product_list, name = 'product_list'),
    path('api/timepackages/', views.timepackage_search, name='timepackage_search'),
    path('cart', views.cart, name = 'cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('pay/', views.pay, name='pay'),
    path('login/', auth_views.LoginView.as_view(template_name='sell_time/login.html'), name='login'),
    path('logout/', views.manual_logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('sell/', views.create_timepackage, name='create_timepackage'),
    path('my-time/', views.my_timepackages, name='my_timepackages'),
#    path('start-checkout/', views.start_checkout, name='start_checkout'),
    path('user-checkout/', views.user_checkout, name='user_checkout'),
    path('guest-checkout/', views.guest_checkout, name='guest_checkout'),
    path('user-pay-success/', views.user_pay_success, name = 'user_pay_success'),
    path('purchases-history/', views.purchase_history, name='purchase_history'),
    ]