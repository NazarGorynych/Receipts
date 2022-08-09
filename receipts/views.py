from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import QueryDict
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm, ReceiptForm
from preferences.models import OrderingPreference
from .models import Receipt, User
from .middleware import get_current_user
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
import json


class IndexView(TemplateView, LoginRequiredMixin, FormMixin):
    template_name = 'receipts_home/index.html'
    form_class = ReceiptForm

    # TO DO LOGIN REQUIRED

    def get_context_data(self, **kwargs):
        preference = OrderingPreference.objects.get(user=get_current_user())
        context_data = super(IndexView, self).get_context_data()

        context_data['users'] = User.objects.all()
        context_data['preference'] = preference
        context_data['receipts'] = preference.retrieve_receipts_by_id()
        return context_data


def sort(request):
    '''
     Reassigns ordered by SortableJS receipts to OrderingPreference,
     and swaps form where it was sorted with the new one to continue the cycle
     '''
    form = ReceiptForm()
    str_ordered_receipts = request.POST.getlist('receipt_order')
    int_ordered_receipts = [int(i) for i in str_ordered_receipts]  # convert str_ordered_receipts to list of integers
    preference = OrderingPreference.objects.get(user_id=get_current_user())
    preference.receipts = int_ordered_receipts
    preference.save()
    receipts = preference.retrieve_receipts_by_id()
    return render(request, 'receipts_home/includes/receipts.html', {'form': form, 'receipts': receipts})


def add_receipt(request):
    if request.method == "POST":
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReceiptForm()
            preference = OrderingPreference.objects.get(user_id=get_current_user())
            receipts = preference.retrieve_receipts_by_id()
            return render(request, 'receipts_home/includes/receipts.html', {'form': form, 'receipts': receipts})
    else:
        form = ReceiptForm()
    return render(request, 'receipts_home/includes/receipt-form.html', {'form': form})


def delete_receipt(request, pk):
    form = ReceiptForm()
    Receipt.objects.get(pk=pk).delete()
    preference = OrderingPreference.objects.get(user_id=get_current_user())
    receipts = preference.retrieve_receipts_by_id()
    return render(request, 'receipts_home/includes/receipts.html', {'form': form, 'receipts': receipts})


def update_receipt(request, pk):
    preference = OrderingPreference.objects.get(user_id=get_current_user())
    receipts = preference.retrieve_receipts_by_id()
    receipt = get_object_or_404(Receipt, pk=pk)
    if request.method == "POST":
        form = ReceiptForm(request.POST or None, instance=receipt)
        if form.is_valid():
            form.save()
            form = ReceiptForm()
            preference = OrderingPreference.objects.get(user_id=get_current_user())
            receipts = preference.retrieve_receipts_by_id()
            return render(request, 'receipts_home/includes/receipts.html', {'form': form, 'receipts': receipts})
    else:
        form = ReceiptForm(instance=receipt)
    return render(request, 'receipts_home/includes/update-receipt.html', {
        'form': form,
        'receipt': receipt,
    })


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        instance = OrderingPreference(user_id=self.object.id)
        instance.save()
        return super(SignUpView, self).get_success_url()
