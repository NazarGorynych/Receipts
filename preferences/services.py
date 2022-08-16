from django.db.models import Max
from preferences.models import OrderingPreference
from .models import Receipt
from django.db import transaction


def get_max_order(user):
    '''Gets the highest number of order in preferences based on the current user (last index) '''
    existing_films = OrderingPreference.objects.filter(user=user)
    if not existing_films.exists():
        return 1
    else:
        current_max = existing_films.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1


def create_new_preference(user, receipt):
    ''''Creates new instances of preferences and assigns indexes them to be the last element'''
    OrderingPreference.objects.create(
        user=user,
        receipt=receipt,
        order=get_max_order(user))


def create_preferences(user, current_receipts, all_receipts):
    '''Creates preferences based on missing links to the receipts '''
    all_receipts_pks = all_receipts.values_list('pk', flat=True)
    current_receipts_pks = current_receipts.all().values_list('receipt_id', flat=True)
    # gets list of instances that the preferences don't have a link to
    difference = [Receipt.objects.get(pk=value) for value in all_receipts_pks if value not in current_receipts_pks]
    for receipt in difference:
        create_new_preference(user, receipt)


def check_integrity_of_indexing(user):
    '''
    Creating preferences if user doesn't have preferences linked to all receipts in the db,
    and then reindexes his preferences to include new connections
    '''
    current_receipts = OrderingPreference.objects.filter(user=user).order_by('order')
    if len(current_receipts) < len(Receipt.get_all_receipts()):
        create_preferences(user, current_receipts, Receipt.get_all_receipts())
        do_reindexing(user, current_receipts)


def do_reindexing(user, current_receipts=None):
    '''
    Reindexes all of the preferences either somebody has added or deleted a receipt,
    if called when receipt is deleted - queries required data, else accepts query
     '''
    if current_receipts is None:
        current_receipts = OrderingPreference.objects.filter(user=user).order_by('order')
    new_ordering = range(1, current_receipts.count() + 1)
    with transaction.atomic():
        for order, ordering_receipt in zip(new_ordering, current_receipts):
            ordering_receipt.order = order
            ordering_receipt.save()
