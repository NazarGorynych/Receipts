from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Receipt(models.Model):
    title = models.CharField(max_length=40)

    @staticmethod
    def get_all_receipts_ids():
        all_receipts = Receipt.objects.all().values_list('pk', flat=True)
        return all_receipts
