#!_*_coding: utf-8 _*_
# @author =  lijun
# date  =  2018/7/3/003 10:37
from django.conf.urls import url

from app import views
from app.views import UserView

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^market/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sort>\d+)/', views.market, name='market'),
    url(r'^add_cart/', views.add_cart, name='add_cart'),
    url(r'^user/', UserView.as_view(), name='user'),
    url(r'^logout/', views.logout, name='logout'),

]




