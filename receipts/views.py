from django.views.generic import CreateView, TemplateView

from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render

from preferences.models import OrderingPreference
from .models import Receipt, User
from .forms import UserCreationForm, ReceiptForm

from .middleware import get_current_user


class IndexView(LoginRequiredMixin, FormMixin, TemplateView):
    template_name = 'receipts_home/index.html'
    form_class = ReceiptForm
    login_url = '/login'

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
    preference = OrderingPreference.objects.get(user_id=get_current_user())
    str_ordered_receipts = request.POST.getlist('receipt_order')
    int_ordered_receipts = [int(i) for i in str_ordered_receipts]  # convert str_ordered_receipts to list of integers
    preference.receipts = int_ordered_receipts
    preference.save()
    return redirect('include-receipts')


def include_receipts(request):
    ''' Include receipts view, used by other views to get dynamic update on receipts in the sortable table '''
    preference = OrderingPreference.objects.get(user_id=get_current_user())
    receipts = preference.retrieve_receipts_by_id()
    form = ReceiptForm()
    return render(request, 'receipts_home/includes/receipts.html', {'form': form, 'receipts': receipts})


def add_receipt(request):
    if request.method == "POST":
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('include-receipts')


def delete_receipt(request, pk):
    Receipt.objects.get(pk=pk).delete()
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
    '''
    Sign up view for user, that creates associated with user preference object
     and fills it with unordered all receipts available
     '''
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        instance = OrderingPreference(user_id=self.object.id)
        instance.save()
        return super(SignUpView, self).get_success_url()
