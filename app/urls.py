#!_*_coding: utf-8 _*_
# @author =  lijun
# date  =  2018/7/3/003 10:37
from django.conf.urls import url

from app import views
from app.views import UserRegisterView, UserLoginView

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^market/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sort>\d+)/', views.market, name='market'),
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^sub_cart_good_num/', views.sub_cart_good_num, name='sub_cart_good_num'),
    url(r'^user/', UserRegisterView.as_view(), name='user'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^checkuser/', views.check_user, name='checkuser'),
    url(r'^user_login/', UserLoginView.as_view(), name='user_login'),

    #邮箱验证
    url(r'active/', views.active, name='active'),
    #改变选中状态
    url(r'changecarts/', views.changecarts, name='changecarts'),
    #改变全选状态
    url(r'changecartliststatus/', views.change_cart_liststatus, name='changecartliststatus'),

    url(r'add_cart_good_num/', views.add_cart_good_num, name='add_cart_good_num'),



]




