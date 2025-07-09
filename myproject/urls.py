# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # For login/logout
    path('subscription/', include('subscriptions.urls')), # Include your subscription app URLs

    # Add this line to redirect the root URL to your subscription detail page
    path('', RedirectView.as_view(url='/subscription/', permanent=True)),
]
