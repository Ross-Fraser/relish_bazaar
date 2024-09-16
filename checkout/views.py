# views.py
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method == 'POST':
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': 'Test Product',
                            },
                            'unit_amount': 2000,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/checkout/success/',
                cancel_url=YOUR_DOMAIN + '/checkout/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'checkout.html')

def checkout_success(request):
    return render(request, 'checkout_success.html')

def checkout_cancel(request):
    return render(request, 'checkout_cancel.html')


