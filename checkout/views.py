# views.py
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    stripe.api_key = 'your-stripe-secret-key'

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_id',  # Use your Stripe price ID
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/checkout/success/'),
            cancel_url=request.build_absolute_uri('/checkout/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def checkout_success(request):
    return render(request, 'checkout_success.html')

def checkout_cancel(request):
    return render(request, 'checkout_cancel.html')


