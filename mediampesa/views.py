import json
import logging
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import requests
from .models import Transactions

logger = logging.getLogger(__name__)

@login_required
def subscription(request):
    """Display subscription plans"""
    return render(request, 'mediampesa/subscription.html')

@login_required
def payment_form(request):
    """Display payment form for subscription"""
    plan = request.GET.get('plan', 'premium')
    amount = request.GET.get('amount', '500')
    return render(request, 'mediampesa/payment_form.html', {
        'plan': plan,
        'amount': amount
    })

@login_required
def stk_push(request):
    """Initiate M-Pesa STK push for subscription payment"""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Validate amount
        try:
            amount = int(amount)
            if amount < 1 or amount > 150000:
                return render(request, 'mediampesa/payment_form.html', {
                    'error': 'Amount must be between KES 1 and 150,000'
                })
        except ValueError:
            return render(request, 'mediampesa/payment_form.html', {
                'error': 'Invalid amount'
            })

        # Validate phone number
        if not phone or len(phone) != 9 or not phone.isdigit():
            return render(request, 'mediampesa/payment_form.html', {
                'error': 'Please enter a valid 9-digit phone number'
            })

        # Get access token
        access_token = get_access_token()
        if not access_token:
            return render(request, 'mediampesa/payment_form.html', {
                'error': 'Payment service temporarily unavailable'
            })

        # Format phone number
        formatted_phone = f"254{phone}"

        # Create transaction record
        transaction = Transactions.objects.create(
            phone_number=formatted_phone,
            amount=amount,
            name=name,
            email=email,
            description='Premium subscription payment',
            status='pending'
        )

        # Prepare STK push payload
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": generate_password(),
            "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": formatted_phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": formatted_phone,
            "CallBackURL": f"{settings.BASE_URL}/mpesa/callback/",
            "AccountReference": f"Premium-{transaction.transaction_id}",
            "TransactionDesc": "Premium subscription payment"
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('ResponseCode') == '0':
                    transaction.checkout_request_id = response_data.get('CheckoutRequestID')
                    transaction.save()
                    return redirect('mpesa:waiting', transaction_id=transaction.transaction_id)
                else:
                    transaction.status = 'failed'
                    transaction.description = response_data.get('ResponseDescription', 'STK push failed')
                    transaction.save()
                    return render(request, 'mediampesa/payment_form.html', {
                        'error': 'Payment initiation failed. Please try again.'
                    })
            else:
                transaction.status = 'failed'
                transaction.description = f'HTTP {response.status_code}'
                transaction.save()
                return render(request, 'mediampesa/payment_form.html', {
                    'error': 'Payment service error. Please try again later.'
                })

        except requests.RequestException as e:
            transaction.status = 'failed'
            transaction.description = str(e)
            transaction.save()
            logger.error(f'STK push error: {str(e)}')
            return render(request, 'mediampesa/payment_form.html', {
                'error': 'Network error. Please try again.'
            })

    return redirect('mpesa:subscription')

@csrf_exempt
def callback(request):
    """Handle M-Pesa callback"""
    try:
        if request.method == 'POST':
            callback_data = json.loads(request.body.decode('utf-8'))

            # Log the callback data
            logger.info(f'M-Pesa Callback: {json.dumps(callback_data, indent=2)}')

            # Extract transaction details
            stk_callback = callback_data.get('Body', {}).get('stkCallback', {})

            if stk_callback:
                merchant_request_id = stk_callback.get('MerchantRequestID')
                checkout_request_id = stk_callback.get('CheckoutRequestID')
                result_code = stk_callback.get('ResultCode')
                result_desc = stk_callback.get('ResultDesc')

                # Find transaction by checkout_request_id
                try:
                    transaction = Transactions.objects.get(checkout_request_id=checkout_request_id)

                    if result_code == 0:
                        # Success
                        callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])

                        # Extract receipt number and transaction date
                        for item in callback_metadata:
                            if item.get('Name') == 'MpesaReceiptNumber':
                                transaction.mpesa_receipt_number = item.get('Value')
                            elif item.get('Name') == 'TransactionDate':
                                # Convert to datetime
                                date_str = str(item.get('Value'))
                                if len(date_str) == 14:
                                    transaction.transaction_date = datetime.strptime(date_str, '%Y%m%d%H%M%S')

                        transaction.status = 'completed'
                        transaction.save()

                        # Update user premium status if this is a subscription payment
                        if transaction.description and 'subscription' in transaction.description.lower():
                            try:
                                from accounts.models import User
                                # Find user by email (assuming email is unique)
                                user = User.objects.get(email=transaction.email)
                                user.is_premium = True
                                # Set premium expiry to 30 days from now
                                from django.utils import timezone
                                from datetime import timedelta
                                user.premium_expiry = timezone.now() + timedelta(days=30)
                                user.save()
                                logger.info(f'User {user.username} upgraded to premium')
                            except User.DoesNotExist:
                                logger.error(f'User with email {transaction.email} not found for premium upgrade')
                            except Exception as e:
                                logger.error(f'Error updating premium status: {str(e)}')

                        logger.info(f'Transaction {transaction.transaction_id} completed successfully')
                    else:
                        # Failed
                        transaction.status = 'failed'
                        transaction.description = result_desc
                        transaction.save()

                        logger.error(f'Transaction {transaction.transaction_id} failed: {result_desc}')

                except Transactions.DoesNotExist:
                    logger.error(f'Transaction not found for callback: {checkout_request_id}')

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

    except Exception as e:
        logger.error(f'Error processing callback: {str(e)}')
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Error processing callback'})

def get_access_token():
    """Get M-Pesa access token"""
    try:
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET

        response = requests.get(
            'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
            auth=(consumer_key, consumer_secret),
            timeout=30
        )

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            logger.error(f'Failed to get access token: {response.status_code}')
            return None
    except Exception as e:
        logger.error(f'Error getting access token: {str(e)}')
        return None

def generate_password():
    """Generate M-Pesa password"""
    import base64
    from datetime import datetime

    shortcode = settings.MPESA_SHORTCODE
    passkey = settings.MPESA_PASSKEY
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    password_str = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode()

    return password

@login_required
def waiting(request, transaction_id):
    """Display waiting page for payment processing"""
    try:
        transaction = Transactions.objects.get(transaction_id=transaction_id, email=request.user.email)
        return render(request, 'mediampesa/waiting.html', {'transaction': transaction})
    except Transactions.DoesNotExist:
        return redirect('mpesa:subscription')

@login_required
def check_status(request, transaction_id):
    """Check transaction status via AJAX"""
    try:
        transaction = Transactions.objects.get(transaction_id=transaction_id, email=request.user.email)
        return JsonResponse({
            'status': transaction.status,
            'description': transaction.description,
            'mpesa_receipt_number': transaction.mpesa_receipt_number
        })
    except Transactions.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)

@login_required
def payment_success(request):
    """Display payment success page"""
    return render(request, 'mediampesa/payment_success.html')

@login_required
def payment_failed(request):
    """Display payment failed page"""
    return render(request, 'mediampesa/payment_failed.html')

@login_required
def payment_cancelled(request):
    """Display payment cancelled page"""
    return render(request, 'mediampesa/payment_cancelled.html')

def index(request):
    """Display M-Pesa index page"""
    return render(request, 'mediampesa/index.html')
