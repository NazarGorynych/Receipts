from django.db import models
from receipts.models import Receipt, User


class OrderingPreference(models.Model):
    '''
    Ordering Preference model that connects Receipt and User and lets User define preferred indexing(ordering) of
    elements in the table
     '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
