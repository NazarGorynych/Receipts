from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm
from preferences.models import OrderingPreference
from .models import Receipt, User
from .middleware import get_current_user
from django.shortcuts import render


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'receipts_home/index.html'

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

    str_ordered_receipts = request.POST.getlist('receipt_order')
    int_ordered_receipts = [int(i) for i in str_ordered_receipts]  # convert str_ordered_receipts to list of integers
    preference = OrderingPreference.objects.get(user_id=get_current_user())
    preference.receipts = int_ordered_receipts
    preference.save()
    receipts = preference.retrieve_receipts_by_id()
    return render(request, 'receipts_home/includes/receipts.html', {'receipts': receipts})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        instance = OrderingPreference(user_id=self.object.id)
        instance.save()
        return super(SignUpView, self).get_success_url()
