# Generated by Django 3.2 on 2021-05-14 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_orderitem_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='digital',
            field=models.BooleanField(default=False, null=True),
        ),
    ]