import hashlib
import time
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from Seller.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 免除CSRF保护


# Create your views here.
def loginValid(fun):
    def inner(request, *args, **kwargs):
        cookie_username = request.COOKIES.get('username')
        session_username = request.session.get('username')
        if cookie_username and session_username and cookie_username == session_username:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Seller/login')

    return inner


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def register(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if not user:
                newuser = LoginUser()
                newuser.email = email
                newuser.username = email
                newuser.password = setPassword(password)
                newuser.save()
                time.sleep(0.5)
                response = HttpResponseRedirect('/Seller/login/')
                return response
            else:
                error_message = '该邮箱已注册，请登录'
        else:
            error_message = '邮箱不可以为空'
    return render(request, 'Seller/register.html', locals())


import datetime
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)  # 设置缓存（缓存寿命）
def login(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        code = request.POST.get('valid_code')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                db_password = user.password
                password = setPassword(password)
                if db_password == password:
                    codes = Value_Code.objects.filter(code_user=email).order_by('-code_time').first()
                    now = time.mktime(datetime.datetime.now().timetuple())
                    db_time = time.mktime(codes.code_time.timetuple())
                    interval = (now - db_time) / 60
                    if codes and codes.code_state == 0 and interval <= 5 and codes.code_content.upper() == code.upper():
                        response = HttpResponseRedirect('/Seller/index/')
                        response.set_cookie('username', user.username)
                        response.set_cookie('userid', user.id)
                        # response.set_cookie('photo',user.photo)
                        request.session['username'] = user.username
                        return response
                    else:
                        error_message = '验证码错误'
                else:
                    error_message = '密码错误'
            else:
                error_message = '该用户不存在'
        else:
            error_message = '邮箱不可以为空'
    return render(request, 'Seller/login.html', locals())


def logout(request):
    response = HttpResponseRedirect('/Seller/login/')
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session['username']
    return response


@loginValid
def index(request):
    return render(request, 'seller/index.html', locals())


@loginValid
def base(request):
    # photo=LoginUser.objects.filter(id=request.user)
    return render(request, 'Seller/base.html', locals())


@loginValid
def goods_list(request, status, page=1):
    page = int(page)
    if status == '1':
        goodses = Goods.objects.filter(goods_status=1)
    elif status == '0':
        goodses = Goods.objects.filter(goods_status=0)
    else:
        goodses = Goods.objects.all()
    all_goods = Paginator(goodses, 10)
    goods_list = all_goods.page(page)
    return render(request, "Seller/goods_list.html", locals())


@loginValid
def goods_add(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == 'POST':
        data = request.POST  # 表单提交的信息
        files = request.FILES  # 图片
        goods = Goods()
        goods.goods_number = data.get('goods_number')
        goods.goods_name = data.get('goods_name')
        goods.goods_price = data.get('goods_price')
        goods.goods_count = data.get('goods_count')
        goods.goods_location = data.get('goods_location')
        goods.goods_safedate = data.get('goods_safedate')
        goods.goods_manufacturedate = data.get('goods_manufacturedate')
        goods.goods_status = 1
        # 保存外键
        goods_type_id = int(data.get('goods_type'))
        goods.goods_type = GoodsType.objects.get(id=goods_type_id)
        # 保存图片
        picture = files.get('picture')
        goods.picture = picture
        # 保存对应卖家
        userid = request.COOKIES.get('userid')
        goods.goods_store = LoginUser.objects.get(id=int(userid))

        goods.save()
    return render(request, 'Seller/goods_add.html', locals())


@loginValid
def goods_status(request, state, id):
    id = int(id)
    goods = Goods.objects.get(id=id)
    if state == 'up':
        goods.goods_status = 1
    elif state == 'down':
        goods.goods_status = 0
    goods.save()
    url = request.META.get('HTTP_REFERER', '/Seller/goods_list/1/1')
    return HttpResponseRedirect(url)


@loginValid
def personal(request):
    userid = request.COOKIES.get('userid')
    user = LoginUser.objects.get(id=int(userid))
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.phonenumber = request.POST.get('phonenumber')
        user.age = request.POST.get('age')
        user.gender = request.POST.get('gender')
        user.address = request.POST.get('address')
        user.photo = request.FILES.get('photo')
        user.save()
    return render(request, 'seller/personal_info.html', locals())


def personal_add(request):
    error_message = ''
    cookie_username = request.COOKIES.get('username')
    if request.method == 'POST':
        if cookie_username:
            username = request.POST.get('username')
            phonenumber = request.POST.get('phonenumber')
            email = request.POST.get('email')
            password = request.POST.get('password')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            photo = request.FILES.get('photo')
            if email:
                user = LoginUser.objects.filter(email=email).first()
                if not user:
                    newuser = LoginUser()
                    newuser.username = username
                    newuser.phonenumber = phonenumber
                    newuser.email = email
                    newuser.password = setPassword(password)
                    newuser.age = age
                    newuser.gender = gender
                    newuser.address = address
                    newuser.photo = photo
                    newuser.save()
                    error_message = '增加成功'
                    # return response
                else:
                    error_message = '邮箱已注册'
            else:
                error_message = '邮箱为空'
        else:
            error_message = '后台须有账户'

    return render(request, 'seller/personal_add.html', locals())


def goods_list_api(request, status, page=1):
    page = int(page)
    if status == "1":
        goodses = Goods.objects.filter(goods_status=1)
    elif status == "0":
        goodses = Goods.objects.filter(goods_status=0)
    else:
        goodses = Goods.objects.all()
    all_goods = Paginator(goodses, 10)
    goods_list = all_goods.page(page)

    res = []
    for g in goods_list:
        res.append({
            "goods_number": g.goods_number,
            "goods_name": g.goods_name,
            "goods_price": g.goods_price,
            "goods_count": g.goods_count,
            "goods_location": g.goods_location,
            "goods_safedate": g.goods_safedate,
            "goods_manufacturedate": g.goods_manufacturedate,
            "goods_status": g.goods_status
        })
    result = {
        "data": res,
        "page_range": list(all_goods.page_range),
        "page": "page"
    }
    return JsonResponse(result)


def order_list(request, status):
    # 0未支付、1已支付、2待收货、3订单完成、4拒收
    status = int(status)
    user_id = request.COOKIES.get('userid')  # 获取店铺id
    store = LoginUser.objects.get(id=user_id)  # 获取店铺信息
    store_order = store.orderinfo_set.filter(order_status=status).order_by('-id')  # 获取店铺对应订单
    return render(request, 'seller/order_list.html', locals())


from Buyer.models import OrderInfo


def change_order(request):
    order_id = request.GET.get('order_id')  # 通过订单id锁定订单详情
    order_status = request.GET.get('order_status')  # 获取要修改的状态
    order = OrderInfo.objects.get(id=order_id)
    order.order_status = int(order_status)
    order.save()
    return JsonResponse({'data': '修改成功'})


import json
import requests
from Retailers.settings import DING_URL


def sendDing(content, to=None):
    headers = {
        'Content-Type': 'application/json',
        'Charset': 'utf-8'
    }
    requests_data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            'atMobiles': [

            ],
            'isAtAll': True
        }
    }
    if to:
        requests_data['at']['atMobiles'].append(to)
        requests_data['at']['isAtAll'] = False
    else:
        requests_data['at']['atMobiles'].clear()
        requests_data['at']['isAtAll'] = True

    sendData = json.dumps(requests_data)
    response = requests.post(url=DING_URL, headers=headers, data=sendData)
    content = response.json()
    return content


import random


def add_goods(request):
    goods_name = "大葱、小葱、蒜、洋葱、生姜、洋姜、莲菜、莴笋、山药、茭白、马铃薯、红薯、卜留克、芦笋（石刁柏）、甘蓝、百合、莲藕、大白菜、小白菜、抱子甘蓝、羽衣甘蓝、紫甘蓝、结球甘蓝、生菜、菠菜、韭菜、芹菜、苦苣、油麦菜、黄秋葵、空心菜、茼蒿、苋菜、香椿、娃娃菜、芥兰、荠菜、香菜、茴香、马齿苋、木耳叶、芥菜、芜荽（大叶香菜、小叶香菜）、雪里蕻、油菜、紫苏、黑芝麻、香椿芽、萝卜芽、荞麦芽、花生芽、姜芽、黄豆芽、绿豆芽、香菇、木耳、草菇、平菇、秀珍菇、金针菇、杏鲍菇、茶树菇、银耳、猴头菇、南瓜、金丝南瓜、黑皮冬瓜、苦瓜、黄瓜、丝瓜、菜瓜、瓠瓜、胡瓜、佛手瓜、西葫芦、番茄、茄子、芸豆、豇豆、豌豆、架豆、刀豆、扁豆、菜豆、毛豆、蛇豆、甜玉米".replace(
        " ", "、")
    goods_name = goods_name.split("、")
    goods_address = "河北，山西，辽宁，吉林，黑龙江，江苏，浙江，安徽，福建，江西，山东，河南，湖北，湖南，广东，海南，四川，贵州，云南，陕西，甘肃，青海，台湾".split("，")
    for j, i in enumerate(range(100), 1):
        goods = Goods()
        goods.goods_number = str(j).zfill(5)
        goods.goods_name = random.choice(goods_address) + random.choice(goods_name)
        goods.goods_price = random.random() * 100
        goods.goods_count = random.randint(30, 100)
        goods.goods_location = random.choice(goods_address)
        goods.goods_safedate = random.randint(1, 36)
        goods.goods_status = 1
        goods.save()
    return HttpResponse("hello world")


def random_code(len=4):  # 验证码随机生成
    string = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    valid_code = ''.join([random.choice(string) for i in range(len)])
    return valid_code


@csrf_exempt
def send_login_code(request):
    result = {
        'code': 200,
        'data': ''
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        code = random_code()
        vc = Value_Code()
        vc.code_user = email
        vc.code_content = code
        vc.save()
        send_data = '%s的验证码是%s,切记不要告诉他人' % (email, code)
        sendDing(send_data)  # 发送验证信息
        result['data'] = '发送成功'
    else:
        result['code'] = 400
        result['data'] = '请求错误'
    return JsonResponse(result)
