from django.db import models
from receipts.models import Receipt, User
from django.contrib.postgres.fields import ArrayField


class OrderingPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receipts = ArrayField(models.IntegerField(), null=True, blank=True)

    def update_receipts(self):
        '''
         Updates current ordering of receipts by adding missing receipts to the list of data,
        or removing deleted receipts from ordering
        '''
        all_receipts = Receipt.get_all_receipts()
        if not self.receipts:
            self.receipts = []
        if len(self.receipts) > len(all_receipts):
            # comprehends which values match and creates list from cross-section
            self.receipts = [value for value in self.receipts if value in all_receipts.values_list('id', flat=True)]
        else:
            # comprehends which values do not match and adds them to a new list
            difference = [value.id for value in all_receipts if value.id not in self.receipts]
            self.receipts += difference


    def retrieve_receipts_by_id(self):
        '''
        Returns list of receipt models from a list of associated IDs,
        if empty returns an empty list
        '''
        self.save()
        receipts_models = []
        if self.receipts:
            for obj_id in self.receipts:
                data = Receipt.objects.get(pk=obj_id)  # get an object to append to the list of models
                receipts_models.append(data)
        return receipts_models

    def save(self, *args, **kwargs):
        self.update_receipts()
        super(OrderingPreference, self).save(*args, **kwargs)
