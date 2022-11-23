from django.urls import path
from . import views


urlpatterns = [
    path("payment/", views.Stripe_Gateway.as_view(), name="payment"),
    path("charge/", views.charge_test, name="charge"),
    
    path("subscriptions/", views.stripe_subscription, name="subscriptions"),
    path("config/", views.stripe_config),
    path("create-checkout-session/", views.create_checkout_session),
]
