from django.contrib import admin
from .models import StripeCustomer

# Register your models here.


@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "stripeCustomerId", "stripeSubscriptionId")
