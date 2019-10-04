from django.urls import path, re_path,include
from Seller.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register/', cache_page(60*15)(register)),
    path('login/', login),
    path('base/', base),
    path('index/', index),
    path('logout/', logout),
    path('goods_list/', goods_list),
    path('goods_add/', goods_add),
    path('personal/', personal),
    path('personal_add/', personal_add),
    # path('add/', add_goods),#增加商品
    re_path('goods_list/(?P<page>\d+)/(?P<status>[01])/', goods_list),
    re_path('goods_status/(?P<state>\w+)/(?P<id>\d+)/', goods_status),

    path('slc/',send_login_code),
    re_path(r'order_list/(?P<status>\d{1})',order_list),
    path('change_order/',change_order)
]
