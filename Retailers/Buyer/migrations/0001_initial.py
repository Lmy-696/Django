# Generated by Django 2.1.8 on 2019-09-11 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Seller', '0005_goodstype_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField()),
                ('goods_picture', models.CharField(max_length=32)),
                ('goods_name', models.CharField(max_length=32)),
                ('goods_count', models.IntegerField()),
                ('goods_price', models.FloatField()),
                ('goods_total_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PayOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=32)),
                ('order_data', models.DateTimeField(auto_now=True)),
                ('order_status', models.IntegerField()),
                ('order_total', models.FloatField(blank=True, null=True)),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser')),
            ],
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.PayOrder'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser'),
        ),
    ]
