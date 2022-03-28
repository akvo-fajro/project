"""SchoolLunchWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

# import view;s from app
from pages.views import homepage_view,login_view,logout_view,profile_view,change_password_view
from menu.views import food_detail_view,food_create_view,forgot_order,pay_money_user_view,\
                    food_delete,order_create_view,cart_view,all_order_view,food_change_view,\
                    be_a_manager,manager_view,money_paying_condition_view,pay_money_manager_view,pay_back_money_view


urlpatterns = [
    path('admin/', admin.site.urls),

    # pages app url's
    path('',homepage_view,name='home'),
    path('accounts/login',login_view,name='login'),
    path('accounts/logout',logout_view,name='logout'),
    path('accounts/profile',profile_view,name='profile'),
    path('accounts/change_password',change_password_view,name='changepassword'),
    path('accounts/pay_money',pay_money_user_view,name='user_pay_money'),

    # menu app url's
    # food in menu
    path('food/detail',food_detail_view,name='detail'),
    path('food/create',food_create_view,name='create'),
    path('food/delete/<int:my_food_id>',food_delete,name='delete'),
    path('food/change/<int:my_food_id>',food_change_view,name='change'),
    # order in menu
    path('food/order/<int:my_food_id>',order_create_view,name='order_create'),
    path('accounts/cart',cart_view,name='cart'),
    # manager in menu
    path('manager/all_order_view',all_order_view,name='all_order_view'),
    path('manager/get_permition',be_a_manager,name='get_permition'),
    path('manager',manager_view,name='manager'),
    path('manager/money_paying',money_paying_condition_view,name='money_paying'),
    path('manager/pay_money/<int:user_id>',pay_money_manager_view,name='pay_money'),
    path('manager/pay_back_money/<int:user_id>',pay_back_money_view,name='pay_back_money'),
    path('manager/forgot_order',forgot_order,name='forgotorder'),
]
