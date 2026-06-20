from django.urls import path
from . import views

app_name = 'business'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('listings/', views.listings, name='listings'),
    
    # Dashboard & Business Management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-business/', views.add_business, name='add_business'),
    path('payment/', views.payment, name='payment'),
    path('payment/paypal-return/', views.paypal_return, name='paypal_return'),
    path('payment/verify-mpesa/', views.verify_mpesa_payment, name='payment-verify-mpesa'),
    
    # Stripe Webhook
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
