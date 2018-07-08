import hashlib

from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.

'''
axf_wheel
'''
class MainWheel(models.Model):
    img = models.CharField(max_length=200, verbose_name='首页轮播图片')
    name = models.CharField(max_length=64, verbose_name='轮播标题')
    trackid = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_wheel'
        verbose_name = '主页轮播图'


class MainNav(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_shop'


class MainShow(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=0)
    categoryid = models.IntegerField(default=0)
    brandname = models.CharField(max_length=64)

    img1 = models.CharField(max_length=200)
    childcid1 = models.IntegerField(default=0)
    productid1 = models.IntegerField(default=0)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.IntegerField(default=0)
    productid2 = models.IntegerField(default=0)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.IntegerField(default=0)
    productid3 = models.IntegerField(default=0)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=16)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.IntegerField(default=0)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=False)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=100)
    dealerid = models.IntegerField(default=0)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):
    u_name = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to='icons')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def set_password(self, password):
        # md5 = hashlib.md5()
        # md5.update(password.encode('utf-8'))
        # password = md5.hexdigest()
        # self.u_password = password
        self.u_password = make_password(password=password)

    def check_password(self, password):
        # md5 = hashlib.md5()
        # md5.update(password.encode('utf-8'))
        # password = md5.hexdigest()
        # return self.u_password == password
        return check_password(password, self.u_password)

    class Meta:
        db_table = 'axf_user'


class Cart(models.Model):
    c_goods = models.ForeignKey(Goods)
    c_user = models.ForeignKey(UserModel)
    is_select = models.BooleanField(default=True)
    c_goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_cart'


class Order(models.Model):
    o_user = models.ForeignKey(UserModel)
    o_total_price = models.FloatField(default=0)
    '''
        需要建立映射
            0代表已下单未付款
            1已下单已付款
            2已下单已付款
            3.。。。。
            
    '''
    o_status = models.IntegerField(default=0)
    o_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'axf_order'


class OrderGoods(models.Model):
    o_order = models.ForeignKey(Order)
    o_goods = models.ForeignKey(Goods)
    o_goods_num = models.IntegerField(default=1)
    class Meta:
        db_table = 'axf_ordergoods'





