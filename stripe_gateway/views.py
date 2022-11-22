from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class Stripe_Gateway(TemplateView):
    template_name = "stripe/payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge_test(request):
    if request.method == "POST":
        # breakpoint()
        charge = stripe.PaymentIntent.create(
            # amount=500,
            # currency="usd",
            # description="payment Gateway",
            # source=request.POST["stripeToken"],
            amount=100,
            currency="inr",
            description="payment Gateway",
            # payment_method_type=["card"],
        )

        return render(request, "stripe/charge.html")
