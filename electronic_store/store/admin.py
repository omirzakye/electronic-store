from django.contrib import admin
from .models import *

admin.site.register(Account)
admin.site.register(Item)
admin.site.register(Department)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
