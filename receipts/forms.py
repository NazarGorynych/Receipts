from django.contrib.auth.forms import UserCreationForm
from .models import Receipt
from django.forms import ModelForm


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
