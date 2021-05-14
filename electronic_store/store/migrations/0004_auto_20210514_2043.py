# Generated by Django 3.2 on 2021-05-14 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_order_orderitem_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='profile',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
