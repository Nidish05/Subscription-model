# subscriptions/models.py

from django.db import models
from django.contrib.auth.models import User # Assuming you're using Django's built-in User model

class Subscription(models.Model):
    """
    Represents a user's subscription plan.
    """
    PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        help_text="The user associated with this subscription."
    )
    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default='Free',
        help_text="The current subscription plan (Free, Basic, Premium)."
    )
    start_date = models.DateField(
        auto_now_add=True, # Automatically sets the date when the object is first created
        help_text="The date when the subscription started."
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="The date when the subscription is set to end (optional)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if the subscription is currently active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the subscription record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, # Automatically updates the date every time the object is saved
        help_text="Timestamp when the subscription record was last updated."
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['-created_at'] # Order by most recent subscriptions first

    def __str__(self):
        """
        String representation of the Subscription object.
        """
        return f"{self.user.username}'s {self.plan} Subscription"

    def save(self, *args, **kwargs):
        """
        Custom save method to ensure is_active is updated based on end_date.
        """
        if self.end_date and self.end_date < models.DateField.today():
            self.is_active = False
        super().save(*args, **kwargs)

    def is_premium(self):
        """
        Helper method to check if the plan is Premium.
        """
        return self.plan == 'Premium' and self.is_active

    def is_basic(self):
        """
        Helper method to check if the plan is Basic.
        """
        return self.plan == 'Basic' and self.is_active
