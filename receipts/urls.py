from django.urls import path
from .views import SignUpView, IndexView, sort

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', IndexView.as_view(), name='index'),
]

htmx_urlpatterns = [
    path('sort/', sort, name='sort'),
]

urlpatterns += htmx_urlpatterns