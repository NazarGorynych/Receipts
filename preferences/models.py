from django.db import models
from receipts.models import Receipt, User


# Create your models here.

class OrderingPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receipts = models.ManyToManyField(Receipt)
