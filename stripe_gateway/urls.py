from django.urls import path
from . import views



urlpatterns = [
    path("payment/", views.Stripe_Gateway.as_view(),name="payment"),
    path("charge/", views.charge_test, name="charge"),
]
