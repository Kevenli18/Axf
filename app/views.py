import uuid
from time import sleep

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, UserModel, Cart
from app.viewhelper import get_user, send_mail_to, get_user_by_id, get_total_price


def home(request):
    # 元信息 获取ip地址
    ip = request.META.get('REMOTE_ADDR')
    result = cache.get(ip + 'home')
    if result:  # 如果缓存中有，就去缓存中拿
        return HttpResponse(result)
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    shop = MainShop.objects.all()
    shop0 = shop[:1]
    shop1_3 = shop[1:3]
    shop3_7 = shop[3:7]
    shop7_11 = shop[7:11]
    mainshows = MainShow.objects.all()
    data = {
        'title': '首页',
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop1_3': shop1_3,
        'shop3_7': shop3_7,
        'shop7_11': shop7_11,
        'mainshows': mainshows,
    }
    # 添加到缓存中, 获取模板
    temp = loader.get_template('home/home.html')
    # 渲染
    result = temp.render(context=data)
    cache.set(ip + 'home', result)
    return HttpResponse(result)

    # return render(request, 'home/home.html', context=data)


@cache_page(120)
def market(request, typeid, cid, sort):
    foodtypes = FoodType.objects.all()
    goods = Goods.objects.all()
    goodslist = goods.filter(categoryid=typeid)

    if cid != '0':  # 点击右上分类
        goodslist = goodslist.filter(childcid=cid)

    """
    全部分类：0#进口水果：110#国产水果：120
    ['','','']
    """
    foodtype = FoodType.objects.get(typeid=typeid)
    childtypenames = foodtype.childtypenames
    childtypename_list = childtypenames.split('#')
    child_type_name_list = []
    for childtypename in childtypename_list:
        child_type_name_list.append(childtypename.split(':'))

    """
    综合排序
        就是对筛选结果进行一个order_by
    服务器能接收对应的字段（排序字段）
    客户端：
    和前端定义接口字段
    """
    if sort == '0':
        pass
    elif sort == '1':
        goodslist = goodslist.order_by('price')
    elif sort == '2':
        goodslist = goodslist.order_by('-price')
    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'typeid': int(typeid),
        'goodslist': goodslist,
        'child_type_name_list': child_type_name_list,
        'cid': cid,
        'sort': sort,
    }
    return render(request, 'market/market.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')

    data = {
        'title': '个人中心',
        'is_login': False,
    }
    if user_id:
        user = UserModel.objects.get(id=user_id)
        data['is_login'] = True
        data['user'] = user
    return render(request, 'mine/mine.html', context=data)


def cart(request):
    user_id = request.session.get('user_id')
    user = get_user_by_id(user_id)
    data = {
        'title': '购物车'
    }
    if not user:
        data['msg'] = '用户未登录'
        return redirect(reverse('axf:user_login'))
    u_carts = user.cart_set.all().filter(c_goods_num__gt=0)
    if not u_carts.filter(is_select=False):
        data['all_select'] = True
    data['u_carts'] = u_carts
    data['total_price'] = get_total_price(user_id)
    return render(request, 'cart/cart.html', context=data)


# 购物车下单,只要有一个没选就不能全选
def changecarts(request):
    cart_id = request.GET.get('cart_id')
    change_cart = Cart.objects.get(id=cart_id)
    change_cart.is_select = not change_cart.is_select   #反选
    change_cart.save()
    all_select = True   #为全选做flag
    user_id = request.session.get('user_id')
    u_carts = Cart.objects.filter(c_user_id=user_id).filter(is_select=False)
    if u_carts:
        all_select = False

    user_id = request.session.get('user_id')
    total_price = get_total_price(user_id)
    data = {
        'status': '200',
        'all_select': all_select,
        'msg': 'ok',
        'is_select': change_cart.is_select,
        'total_price': total_price,
    }
    return JsonResponse(data)


#全选按钮操作
def change_cart_liststatus(request):
    action = request.GET.get('action')
    cart_list = request.GET.get('cart_list')
    carts = cart_list.split('#')
    data = {
        'status': '200',
        'msg': 'change success',
        'action': action
    }
    if action == 'un_select':
        for cart_id in carts:
            u_select_cart = Cart.objects.get(id=cart_id)
            u_select_cart.is_select = True
            u_select_cart.save()
            data['all_select'] = True
    elif action == 'select':
        for cart_id in carts:
            select_cart = Cart.objects.get(id=cart_id)
            select_cart.is_select = False
            select_cart.save()
            data['all_select'] = False
    user_id = request.session.get('user_id')
    total_price = get_total_price(user_id)
    data['total_price'] = total_price
    return JsonResponse(data)


def add_cart(request):
    user_id = request.session.get('user_id')
    user = get_user_by_id(user_id)
    data = {}
    if not user:
        data['msg'] = '未登录'
        data['status'] = '902'  # 用户未登录
        return JsonResponse(data)
    else:
        goodsid = request.GET.get('goodsid')
        u_cart = user.cart_set.filter(c_goods=goodsid)
        if u_cart:
            u_cart = u_cart.first()
            u_cart.c_goods_num = u_cart.c_goods_num + 1
            u_cart.save()
        else:
            u_cart = Cart()
            u_cart.c_user_id = user_id
            u_cart.c_goods_id = goodsid
            u_cart.save()
        data['msg'] = '添加成功'
        data['status'] = '201'
        data['c_goods_num'] = u_cart.c_goods_num
        return JsonResponse(data)


def sub_cart_good_num(request):
    cart_id = request.GET.get('cart_id')
    sub_num = Cart.objects.get(id=cart_id)
    new_num = sub_num.c_goods_num - 1
    if new_num == 0:
        sub_num.delete()
    else:
        sub_num.c_goods_num = new_num
        sub_num.save()
    total_price = get_total_price(user_id=sub_num.c_user_id)
    data = {
        'status': '201',
        'msg': 'add_num success',
        'total_price': total_price,
        'new_num': new_num,
    }
    return JsonResponse(data)


def add_cart_good_num(request):
    cart_id = request.GET.get('cart_id')
    add_num = Cart.objects.get(id=cart_id)
    new_num = add_num.c_goods_num + 1
    add_num.c_goods_num = new_num
    add_num.save()
    total_price = get_total_price(user_id=add_num.c_user_id)
    data = {
        'status': '201',
        'msg': 'add_num success',
        'total_price': total_price,
        'new_num': new_num,
    }
    return JsonResponse(data)


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'user/user_register.html')

    def post(self, request):
        u_username = request.POST.get('u_username', '')
        u_email = request.POST.get('u_email', '')
        u_password = request.POST.get('u_password', '')
        u_icon = request.FILES.get('u_icon', '')
        user = UserModel()
        user.u_name = u_username
        user.set_password(u_password)
        user.u_email = u_email
        user.u_icon = u_icon
        user.save()
        # 生成token ： 时间+ip+随机数   uuid
        token = str(uuid.uuid4())
        cache.set(token, user.id, timeout=60 * 60 * 24)
        active_url = 'http://127.0.0.1:8000/axf/active/?token=' + token
        send_mail_to(u_username, active_url, u_email)
        # request.session['user_id'] = user.id
        response = redirect(reverse('axf:user_login'))
        return response


class UserLoginView(TemplateView):
    # template_name = 'user/user_login.html'  #继承TemplateView，get请求时自动返回页面

    def get(self, request, *args, **kwargs):
        request.session['login_fromm'] = request.META.get('HTTP_REFERER', '/')
        request.session['login_msg'] = ''
        return render(request, 'user/user_login.html')

    def post(self, request):
        username = request.POST.get("u_username")
        password = request.POST.get('u_password')
        user = get_user(username)
        if user:
            if user.check_password(password):
                # 用户密码匹配成功
                request.session['user_id'] = user.id
                if request.session.get('login_from'):
                    return redirect(request.session.get('login_from'))
                return redirect(reverse('axf:mine'))
            else:
                # 密码错误
                request.session['login_msg'] = '用户和密码不匹配！'
                return render(request, 'user/user_login.html')
        # 用户名不存在
        request.session['login_msg'] = '用户不存在！'
        return render(request, 'user/user_login.html')


def logout(request):
    # session和cookie一起清除
    request.session.flush()
    return redirect(reverse('axf:mine'))


def check_user(request):
    username = request.GET.get('username')
    user = get_user(username)
    data = {
        'msg': '用户名可用',
        'status': '200'
    }
    if user:
        data['msg'] = '用户名不可用'
        data['status'] = '901'
    return JsonResponse(data)


def active(request):
    token = request.GET.get('token')
    user_id = cache.get(token)
    if user_id:
        user = UserModel.objects.get(id=user_id)
        user.is_active = True
        user.save()
        request.session['user_id'] = user.id
        return redirect(reverse('axf:mine'))
    else:
        return HttpResponse('激活信息过期，请重新申请激活邮件')
