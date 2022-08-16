from django.views.generic import CreateView, TemplateView

from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render

from preferences.models import OrderingPreference
from .models import Receipt, User
from .forms import UserCreationForm, ReceiptForm

from .middleware import get_current_user

from preferences.services import \
    check_integrity_of_indexing, \
    create_new_preference,\
    do_reindexing

from django.db import transaction


class IndexView(LoginRequiredMixin, FormMixin, TemplateView):
    template_name = 'receipts_home/index.html'
    form_class = ReceiptForm
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context_data = super(IndexView, self).get_context_data()
        check_integrity_of_indexing(get_current_user())
        receipts = OrderingPreference.objects.filter(
            user_id=get_current_user()). \
            prefetch_related('receipt') \
            .order_by('order')

        context_data['users'] = User.objects.all().order_by('date_joined')
        context_data['receipts'] = receipts
        return context_data


def sort(request):
    '''
     Reassigns ordered by SortableJS receipts to OrderingPreference,
     and swaps form where it was sorted with the new one to continue the cycle
     '''
    str_ordered_receipts = request.POST.getlist('receipt_order')
    with transaction.atomic():
        for idx, receipt_id in enumerate(str_ordered_receipts, start=1):
            OrderingPreference.objects.filter(
                user=get_current_user(),
                receipt_id=receipt_id
            ).update(order=idx)
    return redirect('include-receipts')


def include_receipts(request):
    ''' Include receipts view, used by other views to get dynamic update on receipts in the sortable table '''
    receipts = OrderingPreference.objects.filter(
        user_id=get_current_user()). \
        prefetch_related('receipt'). \
        order_by('order')
    form = ReceiptForm()
    return render(request, 'receipts_home/includes/receipts.html', {'form': form, 'receipts': receipts})


def add_receipt(request):
    if request.method == "POST":
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            check_integrity_of_indexing(get_current_user())
            return redirect('include-receipts')


def delete_receipt(request, pk):
    Receipt.objects.get(pk=pk).delete()
    do_reindexing(user=get_current_user())
    return redirect('include-receipts')


def update_receipt(request, pk):
    '''
     Updates receipt based on new data,
     if GET, returns update form for receipt
     '''
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == "POST":
        form = ReceiptForm(request.POST or None, instance=receipt)
        if form.is_valid():
            form.save()
            return redirect('include-receipts')
    else:
        form = ReceiptForm(instance=receipt)
        return render(request, 'receipts_home/includes/update-receipt.html', {
            'form': form,
            'receipt': receipt,
        })


class SignUpView(CreateView):
    '''Sign up view for user, that generates initial preferences with receipts on success'''
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        for receipt in Receipt.get_all_receipts():
            create_new_preference(user=self.object, receipt=receipt)
        return super(SignUpView, self).get_success_url()
