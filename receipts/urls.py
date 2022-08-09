from django.urls import path
from .views import SignUpView, IndexView, sort, add_receipt

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='index'),
]

htmx_urlpatterns = [
    path('sort/', sort, name='sort'),
    path('receipt-form/', add_receipt, name='receipt-form')
]

urlpatterns += htmx_urlpatterns