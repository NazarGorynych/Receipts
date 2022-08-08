from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm
from preferences.models import OrderingPreference
from .models import Receipt, User
from .middleware import get_current_user


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'receipts_home/index.html'

    def get_context_data(self, **kwargs):
        context_data = super(IndexView, self).get_context_data()
        context_data['users'] = User.objects.all()
        preference = OrderingPreference.objects.get(user=get_current_user())
        context_data['receipts'] = preference.retrieve_receipts_by_id()
        return context_data


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        instance = OrderingPreference(user_id=self.object.id)
        instance.save()
        return super(SignUpView, self).get_success_url()
