from django.db import models
from receipts.models import Receipt, User
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class OrderingPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receipts = ArrayField(models.IntegerField(), null=True, blank=True)

    def create_initial_receipts(self):
        '''
         Create temporary Python list to append IDs of receipts,
         and then store it as Integer in an Array in PostgresDB
         Called only on instance initialization
        '''
        all_receipts = Receipt.objects.all()
        temp_lst = []
        for receipt in all_receipts:
            temp_lst.append(receipt.id)
            self.receipts = temp_lst
        return self.receipts

    def retrieve_receipts_by_id(self):
        '''
        Returns list of receipt models from a list of associated IDs,
        if empty returns an empty list
        '''
        receipts_models = []
        if self.receipts:
            for obj_id in self.receipts:
                data = Receipt.objects.get(pk=obj_id)  # get an object to append to the list of models
                receipts_models.append(data)
        return receipts_models

    def save(self, *args, **kwargs):
        if not self.receipts:
            self.create_initial_receipts()
        super(OrderingPreference, self).save(*args, **kwargs)
