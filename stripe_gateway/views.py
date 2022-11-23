from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

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


def stripe_subscription(request):
    return render(request, "stripe/fix_subscription.html")


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/stripe/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id
                if request.user.is_authenticated
                else None,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancel/",
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": settings.STRIPE_PRICE_ID,
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
