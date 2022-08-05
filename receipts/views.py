from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import UserRegisterForm


class SignUpView(CreateView, SuccessMessageMixin):
    form_class = UserRegisterForm
    success_url = reverse_lazy('signup')
    template_name = 'registration/sign-up.html'
    success_message = 'Success!'
