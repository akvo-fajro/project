from django.db import models

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=0)
    popular = models.DecimalField(max_digits=2,decimal_places=0,default=0)
    food_id = models.DecimalField(max_digits=5,decimal_places=0,default=0)


class Order(models.Model):
    food_id = models.DecimalField(max_digits=5,decimal_places=0)
    food_name = models.CharField(max_length=100)
    food_price = models.DecimalField(max_digits=10,decimal_places=0)
    order_sit_number = models.DecimalField(max_digits=2,decimal_places=0)
    number_of_ordering = models.DecimalField(max_digits=1,decimal_places=0,default=0)