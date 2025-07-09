# subscriptions/urls.py (create this file inside your 'subscriptions' app)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_detail, name='subscription_detail'),
    path('update/', views.update_subscription, name='update_subscription'),
]

# In your project's main urls.py (e.g., myproject/urls.py), include these URLs:
# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('django.contrib.auth.urls')), # For login/logout
#     path('subscription/', include('subscriptions.urls')), # Include your subscription app URLs
# ]
