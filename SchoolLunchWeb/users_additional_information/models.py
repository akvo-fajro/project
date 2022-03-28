from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserAdditionalInformation(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    sit_number = models.DecimalField(max_digits=2,decimal_places=0)
    money_to_pay = models.DecimalField(max_digits=10,decimal_places=0,default=0)
    money_pay_back = models.DecimalField(max_digits=10,decimal_places=0,default=0)