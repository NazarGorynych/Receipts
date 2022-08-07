from django.db import models
from receipts.models import Receipt, User


# Create your models here.

class OrderingPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receipts = models.ManyToManyField(Receipt, blank=True, related_name='receipts')

    def save(self, *args, **kwargs):
        super(OrderingPreference, self).save(*args, **kwargs)

        # autoincrement ManyToManyRel with Receipts on new Receipts
        # and on initial user Registration,
        # declared after super(), since pk is needed for ManyToMany
        receipts = Receipt.objects.all()
        self.receipts.add(*receipts)
