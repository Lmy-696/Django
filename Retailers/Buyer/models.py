from django.db import models
from Seller.models import LoginUser

class PayOrder(models.Model):
    order_number=models.CharField(max_length=32)
    order_data=models.DateTimeField(auto_now=True)
    order_status=models.IntegerField()#0未支付、1已支付、2待收货、3订单完成、4拒收
    order_total=models.FloatField(blank=True,null=True)
    order_user=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)


class OrderInfo(models.Model):
    order_id=models.ForeignKey(to=PayOrder,on_delete=models.CASCADE)
    goods_id=models.IntegerField()
    goods_picture=models.CharField(max_length=32)
    goods_name=models.CharField(max_length=32)
    goods_count=models.IntegerField()
    goods_price=models.FloatField()
    goods_total_price=models.FloatField()
    order_status=models.IntegerField(default=0)#0未支付、1已支付、2待收货、3订单完成、4拒收
    store_id=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)

class Cart(models.Model):
    goods_name=models.CharField(max_length=32)#商品名称
    goods_number=models.IntegerField()#商品购买数量
    goods_price=models.FloatField()#商品价格
    goods_picture=models.CharField(max_length=32)#商品图片
    goods_total=models.FloatField()#单个商品总价
    goods_id=models.IntegerField()#商品id
    cart_user=models.IntegerField()#用户

# Create your models here.
