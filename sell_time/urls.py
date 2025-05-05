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
    path('graphs', views.graphs, name = 'graphs'),
    path('pay/', views.pay, name='pay'),
    path('login/', auth_views.LoginView.as_view(template_name='sell_time/login.html'), name='login'),
    path('logout/', views.manual_logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    ]