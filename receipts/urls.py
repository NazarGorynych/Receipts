from django.urls import path
from .views import SignUpView, IndexView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='index'),
]
