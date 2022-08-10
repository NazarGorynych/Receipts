from django.urls import path
from .views import SignUpView, IndexView, sort, add_receipt, delete_receipt, update_receipt, include_receipts

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='index'),
]

htmx_urlpatterns = [
    path('sort/', sort, name='sort'),
    path('receipt-form/', add_receipt, name='receipt-form'),
    path('delete-receipt/<int:pk>/', delete_receipt, name='delete-receipt'),
    path('update-receipt/<int:pk>/', update_receipt, name='update-receipt'),
    path('include-receipts/', include_receipts, name='include-receipts')
]

urlpatterns += htmx_urlpatterns