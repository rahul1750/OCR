from django.urls import path
from webocr import views

app_name = 'webocr'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:cat_no>', views.detail, name='detail'),
    path(r'products/', views.products, name='products'),
    path(r'placeorder/', views.placeorder, name='placeorder'),
    path('product/<int:prod_id>/', views.productdetail, name='productdetail'),
    # path('order_form/', views.place_order, name='order_form'),
    path('order_response/', views.placeorder, name='OrderForm'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('myorders/', views.my_orders, name='myorders'),
    path('register/', views.user_register, name='register'),
    path('forget_password/', views.reset_password, name='forget_password'),
    path('password_changed/', views.reset_password, name='forget_password')

]
