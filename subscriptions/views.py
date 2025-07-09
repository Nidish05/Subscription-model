# subscriptions/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subscription
from .forms import SubscriptionForm
from django.utils import timezone
from datetime import timedelta

@login_required
def subscription_detail(request):
    """
    Displays the current user's subscription details.
    If no subscription exists, it offers to create a default 'Free' one.
    """
    # Try to get the user's subscription, or create a new 'Free' one if it doesn't exist
    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        defaults={'plan': 'Free', 'start_date': timezone.now().date(), 'is_active': True}
    )

    context = {
        'subscription': subscription,
        'created_new': created, # To indicate if a new subscription was just created
    }
    return render(request, 'subscriptions/subscription_detail.html', context)

@login_required
def update_subscription(request):
    """
    Allows the user to update their subscription plan.
    Handles both GET (display form) and POST (process form) requests.
    """
    subscription = get_object_or_404(Subscription, user=request.user)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            # Update start_date if plan changes from Free to a paid plan,
            # or if it's the first time setting a paid plan.
            # This logic can be more complex based on your business rules.
            if subscription.plan == 'Free' and form.cleaned_data['plan'] != 'Free':
                subscription.start_date = timezone.now().date()
                # Example: Set end_date for Basic/Premium plans
                if form.cleaned_data['plan'] == 'Basic':
                    subscription.end_date = timezone.now().date() + timedelta(days=30)
                elif form.cleaned_data['plan'] == 'Premium':
                    subscription.end_date = timezone.now().date() + timedelta(days=365)
                subscription.is_active = True # Ensure active when upgrading

            elif form.cleaned_data['plan'] == 'Free':
                # If downgrading to Free, clear end_date and set active
                subscription.end_date = None
                subscription.is_active = True

            form.save()
            return redirect('subscription_detail')
    else:
        form = SubscriptionForm(instance=subscription)

    context = {
        'form': form,
        'subscription': subscription, # Pass subscription to display current state
    }
    return render(request, 'subscriptions/update_subscription.html', context)

# You'll also need to create a forms.py for the SubscriptionForm
# subscriptions/forms.py
# from django import forms
# from .models import Subscription
#
# class SubscriptionForm(forms.ModelForm):
#     class Meta:
#         model = Subscription
#         fields = ['plan', 'end_date', 'is_active'] # User might not set start_date directly
#         widgets = {
#             'end_date': forms.DateInput(attrs={'type': 'date'}),
#         }
