from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from Seller.models import *
from Seller.views import setPassword
from Buyer.models import *
from alipay import AliPay

import logging
collect=logging.getLogger('django')

def loginValid(fun):
    def inner(request, *args, **kwargs):
        cookie_user = request.COOKIES.get('username')
        session_user = request.session.get('username')
        if cookie_user and session_user and cookie_user == session_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Buyer/login')

    return inner


from django.contrib.auth import authenticate, login


def login(request):
    if request.method == "POST":
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        user = LoginUser.objects.filter(email=email).first()
        if user:
            db_password = user.password
            password = setPassword(password)
            if db_password == password:
                response = HttpResponseRedirect("/Buyer/index/")
                response.set_cookie('username', user.username)
                response.set_cookie('userid', user.id)
                request.session['username'] = user.username

                collect.debug('%s id login'%user.username)

                return response
    return render(request, "buyer/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")

        user = LoginUser()
        user.username = username
        user.password = setPassword(password)
        user.email = email
        user.save()
        return HttpResponseRedirect("/Buyer/login/")
    return render(request, "buyer/register.html")


def index(request):
    goods_type = GoodsType.objects.all()
    result = []
    for ty in goods_type:
        goods = ty.goods_set.order_by('-goods_manufacturedate')
        if len(goods) >= 4:
            goods = goods[:4]
            result.append({'type': ty, 'goods_list': goods})
    return render(request, "buyer/index.html", locals())


def logout(request):
    url = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(url)
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session['username']
    return response


def goods_list(request):
    request_type = request.GET.get('type')  # 获取请求类型，t为类型查询k为关键字查询
    keyword = request.GET.get('keywords')  # 获取查询的内容，类型查id
    goods_list = []
    if request_type == 't':
        if keyword:
            id = int(keyword)
            goods_type = GoodsType.objects.get(id=id)  # 查询类型
            goods_list = goods_type.goods_set.order_by('-goods_manufacturedate')  # 查询类型对应商品
    elif request_type == 'k':
        if keyword:
            goods_list = Goods.objects.filter(goods_name__contains=keyword).order_by('-goods_manufacturedate')
    if goods_list:  # 限定推荐条数
        lenth = len(goods_list) / 5
        if lenth != int(lenth):
            lenth += 1
        lenth = int(lenth)
        recommend = goods_list[:lenth]
    return render(request, 'buyer/goods_list.html', locals())


def goods_detail(request, id):
    goods = Goods.objects.get(id=int(id))
    return render(request, 'buyer/detail.html', locals())


@loginValid
def user_info(request):
    return render(request, 'buyer/user_info.html', locals())


import time
import datetime

@loginValid
def pay_order(request):
    goods_id = request.GET.get('goods_id')
    count = request.GET.get('count')
    if goods_id and count:
        order = PayOrder()
        order.order_number = str(time.time()).replace('.', '')
        order.order_data = datetime.datetime.now()
        order.order_status = 0
        order.order_user = LoginUser.objects.get(id=int(request.COOKIES.get('userid')))  # 订单对应卖家
        order.save()  # 保存订单详情
        goods = Goods.objects.get(id=int(goods_id))  # 查询商品信息
        order_info = OrderInfo()
        order_info.order_id = order
        order_info.goods_id = goods.id
        order_info.goods_picture = goods.picture
        order_info.goods_name = goods.goods_name
        order_info.goods_count = int(count)
        order_info.goods_price = goods.goods_price
        order_info.goods_total_price = goods.goods_price * int(count)
        order_info.order_status = 0
        order_info.store_id = goods.goods_store  # 商品卖家
        order_info.save()
        order.order_total = order_info.goods_total_price
        order.save()
    return render(request, 'buyer/pay_order.html', locals())


def pay_order_more(request):
    data = request.GET
    data_item = data.items()
    request_data = []
    for key, value in data_item:
        if key.startswith('check_'):
            goods_id = key.split('_', 1)[1]
            count = data.get('count_' + goods_id)
            request_data.append((int(goods_id), int(count)))
    if request_data:
        # 保存订单表，总价
        order = PayOrder()
        order.order_number = str(time.time()).replace('.', '')
        order.order_data = datetime.datetime.now()
        order.order_status = 0
        order.order_user = LoginUser.objects.get(id=int(request.COOKIES.get('userid')))
        order.save()
        # 保存订单详情
        order_total = 0
        for goods_id, count in request_data:
            goods = Goods.objects.get(id=int(goods_id))
            order_info = OrderInfo()
            order_info.order_id = order
            order_info.goods_id = goods.id
            order_info.goods_picture = goods.picture
            order_info.goods_name = goods.goods_name
            order_info.goods_count = int(count)
            order_info.goods_price = goods.goods_price
            order_info.goods_total_price = goods.goods_price * int(count)
            order_info.order_status = 0
            order_info.store_id = goods.goods_store
            order_info.save()
            order_total += order_info.goods_total_price  # 总价
        order.order_total = order_total
        order.save()
    return render(request, 'buyer/pay_order.html', locals())


from Retailers.settings import alipay_public_key_string, alipay_private_key_string


def alipayviews(request):
    order_number = request.GET.get('order_number')  # 订单编号
    order_total = request.GET.get('total')  # 支付金额

    # 实例支付
    alipay = AliPay(
        appid='2016101200667742',
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type='RSA2'
    )

    # 实例订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_number,  # 订单号
        total_amount=str(order_total),  # 支付金额-字符串
        subject='百货商店',  # 支付主题
        return_url='http://127.0.0.1:8000/Buyer/pay_result/',  # 支付结果返回地址
        notify_url='http://127.0.0.1:8000/Buyer/pay_result/'  # 订单状态发生改变返回地址
    )

    result = 'https://openapi.alipaydev.com/gateway.do?' + order_string

    return HttpResponseRedirect(result)


def pay_result(request):
    out_trage_no = request.GET.get('out_trade_no')
    if out_trage_no:
        order = PayOrder.objects.get(order_number=out_trage_no)#总订单号
        order.order_status = 1
        order.save()
        order.orderinfo_set.all().update(order_status=1)
    return render(request, 'buyer/pay_result.html', locals())


@loginValid
def add_cart(request):
    result = {
        'code': 200,
        'data': ''
    }
    if request.method == 'POST':
        id = int(request.POST.get('goods_id'))
        count = int(request.POST.get('count', 1))
        goods = Goods.objects.get(id=id)
        cart = Cart()
        cart.goods_name = goods.goods_name
        cart.goods_number = count
        cart.goods_price = goods.goods_price
        cart.goods_picture = goods.picture
        cart.goods_total = goods.goods_price * count
        cart.goods_id = id
        cart.cart_user = request.COOKIES.get('userid')
        cart.save()
        result['data'] = '加入购物车成功'
    else:
        result['code'] = 500
        result['data'] = '请求方式错误'
    return JsonResponse(result)


@loginValid
def cart(request):
    user_id = request.COOKIES.get('userid')
    goods = Cart.objects.filter(cart_user=int(user_id)).order_by('-id')  # 倒排序
    count = goods.count()
    return render(request, 'buyer/cart.html', locals())

def deleat_cart(request,goods_id):
    id=request.COOKIES.get('userid')
    goods=Cart.objects.filter(cart_user=int(id),goods_id=int(goods_id))
    goods.delete()
    return HttpResponseRedirect('/Buyer/cart/')


@loginValid
def user_cent_order(request):
    user_id = request.COOKIES.get('userid')
    user = LoginUser.objects.get(id=int(user_id))
    order_list = user.payorder_set.order_by('-order_data')
    return render(request, 'buyer/user_center_order.html', locals())


from CeleryTask.tasks import add

def get_tesk(request):
    # taskExample.delay()发布任务
    x = request.GET.get('x', 6)
    y = request.GET.get('y', 6)
    add.delay(int(x), int(y))
    return JsonResponse({'data': 'sccess'})


from django.http import HttpResponse


def middle_test_view(request):
    def hello():
        return HttpResponse('hello world')

    rep = HttpResponse('hello')
    rep.render = hello
    return rep


from django.core.cache import cache
def cacheTest(request):
    user=cache.get('user')#从缓存里获取用户
    if not user:
        user=LoginUser.objects.get(id=1)
        cache.set('user',user,30)#将用户数据存入缓存，缓存时间30秒
    return JsonResponse({'data':'hello'})



# Create your views here.
