from django.db import models


# Create your models here.

class Department(models.Model):
    dep_name = models.CharField(max_length=255)

    def __str__(self):
        return self.dep_name


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_desc = models.TextField('item_desc')
    item_cost = models.IntegerField()
    item_quantity = models.IntegerField(default=0)
    item_rate = models.FloatField(default=0.0)
    num_of_views = models.IntegerField(default=0)
    dep_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_name} ({self.dep_id})"


class Customer(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    bonus = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} {self.surname}"
