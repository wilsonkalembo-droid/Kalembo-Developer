"""
Payment Service Module
Handles PayPal and M-Pesa payment processing
"""

import paypalrestsdk
import requests
import json
import base64
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from .models import Payment


class PayPalPaymentService:
    """Handle PayPal payment processing"""
    
    def __init__(self):
        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRET,
        })
    
    def create_payment(self, business, return_url, cancel_url):
        """Create a PayPal payment"""
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {
                'payment_method': 'paypal'
            },
            'redirect_urls': {
                'return_url': return_url,
                'cancel_url': cancel_url
            },
            'transactions': [{
                'item_list': {
                    'items': [{
                        'name': f'SokoConnect Business Listing - {business.business_name}',
                        'sku': f'LISTING-{business.id}',
                        'price': settings.PAYPAL_BUSINESS_LISTING_PRICE,
                        'currency': settings.PAYPAL_CURRENCY,
                        'quantity': 1
                    }]
                },
                'amount': {
                    'total': settings.PAYPAL_BUSINESS_LISTING_PRICE,
                    'currency': settings.PAYPAL_CURRENCY,
                    'details': {
                        'subtotal': settings.PAYPAL_BUSINESS_LISTING_PRICE,
                        'tax': '0',
                        'shipping': '0'
                    }
                },
                'description': 'Business listing fee for SokoConnect platform',
                'invoice_number': f'INV-{business.id}-{datetime.now().timestamp()}'
            }]
        })
        
        if payment.create():
            return {'success': True, 'payment_id': payment.id, 'approval_url': payment.links[1].href}
        else:
            return {'success': False, 'error': payment.error['message']}
    
    def execute_payment(self, payment_id, payer_id, business):
        """Execute a PayPal payment after user approval"""
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({'payer_id': payer_id}):
            # Save payment to database
            Payment.objects.create(
                business=business,
                amount=settings.PAYPAL_BUSINESS_LISTING_PRICE,
                payment_method='paypal',
                status='completed',
                transaction_id=payment.id
            )
            return {'success': True, 'transaction_id': payment.id}
        else:
            return {'success': False, 'error': payment.error['message']}


class MPesaPaymentService:
    """Handle M-Pesa payment processing via Safaricom Daraja API"""
    
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        
        if settings.MPESA_ENVIRONMENT == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def get_access_token(self):
        """Get M-Pesa access token"""
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        
        auth_string = f'{self.consumer_key}:{self.consumer_secret}'
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {auth_base64}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception('Failed to get M-Pesa access token')
    
    def initiate_stk_push(self, phone_number, amount, business, callback_url, network='mpesa'):
        """Initiate mobile money STK push for payment (M-Pesa, Airtel Money, Tigo Pesa)"""
        try:
            # Map networks to their configurations
            network_config = {
                'mpesa': {
                    'name': 'M-Pesa',
                    'shortcode': self.shortcode,
                    'passkey': self.passkey
                },
                'airtel_money': {
                    'name': 'Airtel Money',
                    'shortcode': self.shortcode,  # Would need separate config
                    'passkey': self.passkey
                },
                'tigo_pesa': {
                    'name': 'Tigo Pesa',
                    'shortcode': self.shortcode,  # Would need separate config
                    'passkey': self.passkey
                }
            }
            
            config = network_config.get(network, network_config['mpesa'])
            access_token = self.get_access_token()
            
            url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Create password for STK push
            password_string = f'{config["shortcode"]}{config["passkey"]}{timestamp}'
            password_bytes = password_string.encode('utf-8')
            password_base64 = base64.b64encode(password_bytes).decode('utf-8')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': config['shortcode'],
                'Password': password_base64,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': int(amount),
                'PartyA': phone_number,
                'PartyB': config['shortcode'],
                'PhoneNumber': phone_number,
                'CallBackURL': callback_url,
                'AccountReference': f'LISTING-{business.id}',
                'TransactionDesc': f'Business listing fee - {business.business_name}'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('ResponseCode') == '0':
                    return {
                        'success': True,
                        'checkout_request_id': response_data.get('CheckoutRequestID'),
                        'response_code': response_data.get('ResponseCode'),
                        'response_description': response_data.get('ResponseDescription'),
                        'network': network
                    }
                else:
                    return {
                        'success': False,
                        'error': response_data.get('ResponseDescription', 'STK push failed')
                    }
            else:
                return {'success': False, 'error': 'Failed to initiate STK push'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def verify_payment(self, merchant_request_id, checkout_request_id, business):
        """Verify M-Pesa payment status"""
        try:
            access_token = self.get_access_token()
            
            url = f'{self.base_url}/mpesa/stkpushquery/v1/query'
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # Create password
            password_string = f'{self.shortcode}{self.passkey}{timestamp}'
            password_bytes = password_string.encode('utf-8')
            password_base64 = base64.b64encode(password_bytes).decode('utf-8')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'BusinessShortCode': self.shortcode,
                'Password': password_base64,
                'Timestamp': timestamp,
                'CheckoutRequestID': checkout_request_id
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Check if payment was successful (ResultCode == 0)
                if response_data.get('ResultCode') == 0:
                    # Save payment to database
                    Payment.objects.create(
                        business=business,
                        amount=settings.MPESA_BUSINESS_LISTING_PRICE,
                        payment_method='mpesa',
                        status='completed',
                        transaction_id=response_data.get('MpesaReceiptNumber', checkout_request_id)
                    )
                    return {'success': True, 'transaction_id': response_data.get('MpesaReceiptNumber')}
                else:
                    return {
                        'success': False,
                        'result_code': response_data.get('ResultCode'),
                        'result_description': response_data.get('ResultDesc', 'Payment verification pending')
                    }
            else:
                return {'success': False, 'error': 'Failed to verify payment'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
