# subscriptions/forms.py

from django import forms
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    """
    Form for updating a user's subscription.
    """
    class Meta:
        model = Subscription
        # Fields that the user can directly modify
        fields = ['plan', 'end_date', 'is_active']
        widgets = {
            # Use HTML5 date input for better user experience
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input rounded-md shadow-sm mt-1 block w-full'}),
            'plan': forms.Select(attrs={'class': 'form-select rounded-md shadow-sm mt-1 block w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'})
        }
        labels = {
            'plan': 'Subscription Plan',
            'end_date': 'Subscription End Date',
            'is_active': 'Is Subscription Active?',
        }
