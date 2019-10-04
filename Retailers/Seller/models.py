from django.db import models


class LoginUser(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=32)

    username=models.CharField(max_length=32,null=True,blank=True)
    phonenumber=models.CharField(max_length=32,null=True,blank=True)
    photo=models.ImageField(upload_to='images',default='images/default.png')
    age=models.IntegerField(null=True,blank=True)
    gender=models.CharField(max_length=32,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    url_type=models.IntegerField(default=0)#买家0，卖家1，管理员2

class GoodsType(models.Model):
    type_label=models.CharField(max_length=32)
    type_description=models.TextField()
    picture = models.ImageField(upload_to="images")

class Goods(models.Model):
    goods_number=models.CharField(max_length=11)
    goods_name=models.CharField(max_length=32)
    goods_price=models.FloatField()
    goods_count=models.IntegerField()
    goods_location=models.CharField(max_length=256)
    goods_safedate=models.IntegerField()#保质期
    goods_manufacturedate=models.DateField(auto_now=True)#生产日期
    goods_status = models.IntegerField() #0为下架，1 为在售

    picture=models.ImageField(upload_to='images')
    goods_type=models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,default=1)
    goods_store=models.ForeignKey(to=LoginUser,on_delete=models.CASCADE,default=1)

class Value_Code(models.Model):#验证码
    code_content=models.CharField(max_length=32)#验证码内容
    code_user=models.EmailField()
    code_time=models.DateTimeField(auto_now=True)
    code_state=models.IntegerField(default=0)#0未使用，1已使用

# Create your models here.
