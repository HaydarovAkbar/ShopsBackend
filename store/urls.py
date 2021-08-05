from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('categories/', views.categories, name = 'categories'),
    path('categories/<int:cat_id>/', views.products, name = 'categories'),
    path('client_orders/<int:id>/', views.user_cart, name = 'categories'),
    path('cart/', views.cart, name = 'cart'),
    path('update_details/', views.update_details, name = 'update_detail'),
    path('user/', views.user_form, name = 'user'),
    path('login/', views.log_in, name = 'login'),
    path('logout/', views.log_out, name = 'logout'),
    path('product_form/', views.product_form, name = 'product_form'),
    path('client_orders/', views.client_orders, name = 'client_orders'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]