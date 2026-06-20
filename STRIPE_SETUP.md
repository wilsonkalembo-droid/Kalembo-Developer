# Stripe Payment Integration Setup Guide

## Overview
SokoConnect now uses **Stripe** for real payment processing. Follow these steps to get your payment system working.

## Step 1: Create a Stripe Account
1. Go to https://stripe.com
2. Sign up for a new account (or login if you already have one)
3. Complete the signup process

## Step 2: Get Your API Keys
1. Log into your Stripe Dashboard
2. Go to **Developers** → **API Keys**
3. You'll see two types of keys:
   - **Publishable Key** (starts with `pk_test_` or `pk_live_`)
   - **Secret Key** (starts with `sk_test_` or `sk_live_`)

## Step 3: Configure Environment Variables
Open `SokoConnect/settings.py` and update these settings:

```python
# Replace with your actual keys from Stripe Dashboard
STRIPE_PUBLIC_KEY = 'pk_test_YOUR_PUBLIC_KEY_HERE'
STRIPE_SECRET_KEY = 'sk_test_YOUR_SECRET_KEY_HERE'
STRIPE_WEBHOOK_SECRET = 'whsec_test_YOUR_WEBHOOK_SECRET_HERE'
STRIPE_BUSINESS_LISTING_PRICE = 5000  # $50.00 in cents
STRIPE_CURRENCY = 'usd'
```

## Step 4: Set Up Webhooks (Important for Production)
1. In Stripe Dashboard, go to **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Set the endpoint URL to: `https://yourdomain.com/stripe/webhook/`
4. Select events to listen for:
   - `checkout.session.completed`
5. Copy the **Signing Secret** and update `STRIPE_WEBHOOK_SECRET` in settings.py

## Step 5: Test the Payment System

### Using Test Cards:
Stripe provides test card numbers for development:
- **Test Card**: 4242 4242 4242 4242
- **Expiry**: Any future date (e.g., 12/25)
- **CVC**: Any 3 digits (e.g., 123)

### Steps to Test:
1. Start the Django server: `python manage.py runserver`
2. Register a test account
3. Add business details
4. Click "Complete Payment"
5. You'll be redirected to Stripe Checkout
6. Use the test card numbers above
7. Complete the checkout
8. You should be redirected back to your dashboard

## Step 6: Deployment Checklist

### Before Going Live:
1. Switch to **Live Keys** from your Stripe Dashboard
2. Update `settings.py` with live API keys
3. Update webhook URL to your production domain
4. Set `DEBUG = False` in settings.py
5. Update `ALLOWED_HOSTS` with your domain
6. Set up HTTPS (required for production)

### Important Files Updated:
- `business/views.py` - Stripe payment handling
- `SokoConnect/settings.py` - Stripe configuration
- `business/urls.py` - Webhook URL endpoint
- `templates/payment.html` - Payment UI

## Payment Flow

1. **User Registration & Business Setup**
   - User creates account and adds business details
   - Status: `draft` → `pending_payment`

2. **Payment Initiation**
   - User clicks "Complete Payment"
   - Django creates Stripe checkout session
   - User redirected to Stripe checkout page

3. **Payment Processing**
   - User enters payment details (test card or real)
   - Stripe processes payment securely
   - Stripe sends webhook confirmation

4. **Payment Confirmation**
   - Webhook handler receives `checkout.session.completed` event
   - Payment record created in database
   - Business status updated to `payment_done`
   - User redirected to dashboard

5. **Admin Review**
   - Admin reviews payment and business details
   - Admin approves or rejects listing
   - User receives notification

## Troubleshooting

### "STRIPE_PUBLIC_KEY not found"
- Make sure you've added the keys to `settings.py`
- Restart Django server after changes

### Webhook not working
- Check webhook URL is correct in Stripe Dashboard
- Verify webhook secret in `settings.py`
- Check server logs for errors

### Payment fails
- Use test card: 4242 4242 4242 4242
- Check Stripe Dashboard logs for error details
- Make sure `STRIPE_CURRENCY` matches your region

## Security Notes
- **Never commit API keys** to version control
- Use environment variables for production
- Always use HTTPS in production
- Keep webhook secret secure
- Monitor Stripe Dashboard for suspicious activity

## Contact & Support
For Stripe support: https://support.stripe.com
For SokoConnect issues: Check the admin dashboard or contact support team
