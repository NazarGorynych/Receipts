from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # index and sign-up
    path('', include('receipts.urls')),

    # authentication
    path('', include('django.contrib.auth.urls')),

]
