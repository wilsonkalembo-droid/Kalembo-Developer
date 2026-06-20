from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import BusinessListing, Payment, CATEGORY_CHOICES
from .payment_service import PayPalPaymentService, MPesaPaymentService
import json
import stripe
from decimal import Decimal

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    """Render the home page"""
    context = {
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)


def register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('business:dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        business_name = request.POST.get('business_name', '')
        business_category = request.POST.get('business_category', '')
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not all([first_name, last_name, email, business_name, business_category, phone, password, confirm_password]):
            errors.append('All fields are required')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        
        if User.objects.filter(email=email).exists():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create user
            username = email.split('@')[0]
            if User.objects.filter(username=username).exists():
                username = email
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create business listing
            business = BusinessListing.objects.create(
                user=user,
                business_name=business_name,
                category=business_category,
                phone=phone,
                email=email
            )
            
            # Login user
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('business:add_business')
    
    context = {
        'page_title': 'Register',
        'categories': CATEGORY_CHOICES,
    }
    return render(request, 'register.html', context)


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('business:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate with email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('business:dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    
    context = {
        'page_title': 'Login',
    }
    return render(request, 'login.html', context)


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('business:home')


@login_required(login_url='business:login')
def dashboard(request):
    """User dashboard"""
    try:
        business = BusinessListing.objects.get(user=request.user)
    except BusinessListing.DoesNotExist:
        return redirect('business:add_business')
    
    payments = Payment.objects.filter(business=business).order_by('-created_at')
    
    context = {
        'page_title': 'Dashboard',
        'business': business,
        'payments': payments,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='business:login')
def add_business(request):
    """Add or edit business details"""
    if not request.user.is_authenticated:
        return redirect('business:login')
    
    try:
        business = BusinessListing.objects.get(user=request.user)
        is_edit = True
    except BusinessListing.DoesNotExist:
        business = None
        is_edit = False
    
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        category = request.POST.get('business_category')
        description = request.POST.get('description')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        location = request.POST.get('location')
        website = request.POST.get('website')
        logo = request.FILES.get('logo')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        price_unit = request.POST.get('price_unit')
        operating_hours = request.POST.get('operating_hours')
        requirements = request.POST.get('requirements')
        
        if not business:
            business = BusinessListing.objects.create(user=request.user)
        
        business.business_name = business_name
        business.category = category
        business.description = description
        business.phone = phone
        business.email = email
        business.location = location
        business.website = website
        business.min_price = min_price if min_price else None
        business.max_price = max_price if max_price else None
        business.price_unit = price_unit if price_unit else 'per item'
        business.operating_hours = operating_hours
        business.requirements = requirements
        if logo:
            business.logo = logo
        business.status = 'pending_payment'
        business.save()
        
        messages.success(request, 'Business details saved! Proceed to payment.')
        return redirect('business:payment')
    
    context = {
        'page_title': 'Add/Edit Business',
        'business': business,
        'categories': CATEGORY_CHOICES,
        'is_edit': is_edit,
    }
    return render(request, 'add_business.html', context)


@login_required(login_url='business:login')
def payment(request):
    """Payment page for business listing - PayPal & M-Pesa Integration"""
    try:
        business = BusinessListing.objects.get(user=request.user)
    except BusinessListing.DoesNotExist:
        return redirect('business:add_business')
    
    # Check if already paid
    completed_payment = Payment.objects.filter(
        business=business,
        status='completed'
    ).exists()
    
    if completed_payment:
        messages.info(request, 'Payment already completed! Your business is pending review.')
        return redirect('business:dashboard')
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'paypal')
        
        try:
            if payment_method == 'paypal':
                # PayPal payment initialization
                paypal_service = PayPalPaymentService()
                return_url = request.build_absolute_uri('/payment/paypal-return/')
                cancel_url = request.build_absolute_uri('/payment/?payment_cancelled=true')
                
                payment_result = paypal_service.create_payment(business, return_url, cancel_url)
                
                if payment_result['success']:
                    # Store payment ID in session for later verification
                    request.session['paypal_payment_id'] = payment_result['payment_id']
                    request.session['business_id'] = business.id
                    return redirect(payment_result['approval_url'])
                else:
                    messages.error(request, f'PayPal error: {payment_result["error"]}')
                    return redirect('business:payment')
            
            elif payment_method in ['mpesa', 'airtel_money', 'tigo_pesa']:
                # Mobile money payment initialization (M-Pesa, Airtel Money, Tigo Pesa)
                phone_number = request.POST.get('mobile_money_phone', '')
                
                if not phone_number:
                    messages.error(request, 'Please enter your phone number')
                    return redirect('business:payment')
                
                mpesa_service = MPesaPaymentService()
                callback_url = request.build_absolute_uri('/api/mpesa-callback/')
                
                payment_result = mpesa_service.initiate_stk_push(
                    phone_number,
                    settings.MPESA_BUSINESS_LISTING_PRICE,
                    business,
                    callback_url,
                    payment_method  # Pass network type to service
                )
                
                if payment_result['success']:
                    # Store checkout request ID for later verification
                    request.session['mpesa_checkout_id'] = payment_result['checkout_request_id']
                    request.session['business_id'] = business.id
                    request.session['payment_network'] = payment_method
                    
                    network_names = {
                        'mpesa': 'M-Pesa',
                        'airtel_money': 'Airtel Money',
                        'tigo_pesa': 'Tigo Pesa'
                    }
                    network_name = network_names.get(payment_method, 'Mobile Money')
                    
                    messages.success(request, f'STK push sent to {phone_number}. Please enter your {network_name} PIN to complete payment.')
                    return redirect('business:payment-verify-mpesa')
                else:
                    messages.error(request, f'Payment error: {payment_result["error"]}')
                    return redirect('business:payment')
        
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('business:payment')
    
    context = {
        'page_title': 'Payment',
        'business': business,
        'paypal_amount': settings.PAYPAL_BUSINESS_LISTING_PRICE,
        'mpesa_amount': settings.MPESA_BUSINESS_LISTING_PRICE,
        'paypal_currency': settings.PAYPAL_CURRENCY,
        'mpesa_currency': settings.MPESA_CURRENCY,
    }
    return render(request, 'payment.html', context)


@login_required(login_url='business:login')
def paypal_return(request):
    """PayPal return/callback handler"""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    if not payment_id or not payer_id:
        messages.error(request, 'Payment was cancelled')
        return redirect('business:payment')
    
    try:
        business = BusinessListing.objects.get(user=request.user)
        paypal_service = PayPalPaymentService()
        
        result = paypal_service.execute_payment(payment_id, payer_id, business)
        
        if result['success']:
            # Update business status
            business.status = 'payment_done'
            business.save()
            
            messages.success(request, 'Payment successful! Your business has been submitted for review.')
            return redirect('business:dashboard')
        else:
            messages.error(request, f'Payment error: {result["error"]}')
            return redirect('business:payment')
    
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('business:payment')


@login_required(login_url='business:login')
def verify_mpesa_payment(request):
    """Verify M-Pesa payment status"""
    checkout_id = request.session.get('mpesa_checkout_id')
    
    if not checkout_id:
        messages.error(request, 'Payment session not found')
        return redirect('business:payment')
    
    try:
        business = BusinessListing.objects.get(user=request.user)
        mpesa_service = MPesaPaymentService()
        
        # Verify the payment
        result = mpesa_service.verify_payment(None, checkout_id, business)
        
        if result['success']:
            # Update business status
            business.status = 'payment_done'
            business.save()
            
            # Clear session safely
            request.session.pop('mpesa_checkout_id', None)
            request.session.pop('business_id', None)
            
            messages.success(request, f'Payment successful! Transaction ID: {result["transaction_id"]}')
            return redirect('business:dashboard')
        else:
            # Payment might still be processing
            result_code = result.get('result_code')
            if result_code in [2001, 1001]:  # Request in progress or timeout
                messages.warning(request, 'Payment is still processing. Please try again in a moment.')
            else:
                messages.error(request, f'Payment failed: {result.get("result_description", "Unknown error")}')
            
            return redirect('business:payment')
    
    except Exception as e:
        messages.error(request, f'Error verifying payment: {str(e)}')
        return redirect('business:payment')


def contact(request):
    """Render the contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        business_name = request.POST.get('business_name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email to admin
        try:
            send_mail(
                subject=f'SokoConnect Contact: {subject}',
                message=f'From: {name} ({email})\nPhone: {phone}\nBusiness: {business_name}\n\nMessage:\n{message}',
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@sokoconnect.com',
                recipient_list=['admin@sokoconnect.com'],
                fail_silently=True,
            )
        except Exception as e:
            pass  # Fail silently
        
        messages.success(request, 'Message sent! We will contact you soon.')
        return redirect('business:contact')
    
    context = {
        'page_title': 'Contact Us',
    }
    return render(request, 'contact.html', context)


def about(request):
    """Render the about page"""
    context = {
        'page_title': 'About Us',
    }
    return render(request, 'about.html', context)


def listings(request):
    """Display all approved business listings"""
    category_filter = request.GET.get('category', '')
    
    # Get all approved businesses
    approved_businesses = BusinessListing.objects.filter(
        status='approved'
    ).select_related('user').order_by('-created_at')
    
    # Filter by category if provided
    if category_filter:
        approved_businesses = approved_businesses.filter(category=category_filter)
    
    context = {
        'page_title': 'Business Listings',
        'businesses': approved_businesses,
        'categories': CATEGORY_CHOICES,
        'selected_category': category_filter,
        'total_businesses': approved_businesses.count(),
    }
    return render(request, 'listings.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events for payment confirmation"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Get business and user info from metadata
        business_id = session['metadata'].get('business_id')
        
        try:
            business = BusinessListing.objects.get(id=business_id)
            
            # Create payment record
            payment = Payment.objects.create(
                business=business,
                amount=Decimal(session['amount_total'] / 100),  # Convert from cents
                payment_method='stripe',
                status='completed',
                transaction_id=session['id']
            )
            
            # Update business status
            business.status = 'payment_done'
            business.save()
            
        except BusinessListing.DoesNotExist:
            pass
    
    return JsonResponse({'status': 'success'}, status=200)
