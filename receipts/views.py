from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreationForm
from preferences.models import OrderingPreference


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'receipts_home/index.html'


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        instance = OrderingPreference(user_id=self.object.id)
        instance.save()
        return super(SignUpView, self).get_success_url()
