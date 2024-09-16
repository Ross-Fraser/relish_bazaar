from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('checkout/', views.create_checkout_session, name='create_checkout_session'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
]
