from django.urls import path, re_path,include
from Buyer.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('logout/', logout),
    path('goods_list/', goods_list),
    re_path('goods_detail/(?P<id>\d+)/', goods_detail),
    path('user_info/',user_info),
    path('pay_order/',pay_order),
    path('pay_order_more/',pay_order_more),
    path('alipay/',alipayviews),
    path('pay_result/',pay_result),
    path('add_cart/',add_cart),
    path('cart/',cart),
    re_path('deleat_cart/(?P<goods_id>\d+)',deleat_cart),
    path('uco/',user_cent_order),
    path('gt/',get_tesk),
    path('mtv/',middle_test_view),
]