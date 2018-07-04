from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, UserModel


def home(request):
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
    return render(request, 'home/home.html', context=data)


def market(request, typeid, cid, sort):
    foodtypes = FoodType.objects.all()
    goods = Goods.objects.all()
    goodslist = goods.filter(categoryid=typeid)

    if cid != '0':    #点击右上分类
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


def cart(request):

    data = {
        'title': '购物车'
    }
    return render(request, 'cart/cart.html', context=data)


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


def add_cart(request):

    return JsonResponse


class UserView(View):
    def get(self, request):
        return render(request, 'user/user_register.html')

    def post(self, request):
        u_username = request.POST.get('u_username', '')
        u_email = request.POST.get('u_email', '')
        u_password = request.POST.get('u_password', '')
        u_icon = request.FILES.get('u_icon', '')
        user = UserModel()
        user.u_name = u_username
        user.u_password = u_password
        user.u_email = u_email
        user.u_icon = u_icon
        user.save()
        request.session['user_id'] = user.id
        response = redirect(reverse('axf:mine'))
        return response


def logout(request):
    #session和cookie一起清除
    request.session.flush()
    return redirect(reverse('axf:mine'))








