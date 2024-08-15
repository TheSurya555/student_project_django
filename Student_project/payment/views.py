from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPAuthenticationError
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from .models import Payment, Profile, Subscription
from signUp.models import CustomUser  # Adjust the import according to your project structure
import logging
from decimal import Decimal
import razorpay

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

logger = logging.getLogger(__name__)

@login_required
def payment_page(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Convert subscription price to Decimal if necessary (depending on your model definition)
    subscription_price = Decimal(subscription.price)
    
    # Calculate service fee and GST based on subscription price (using Decimal)
    service_fee = subscription_price * Decimal('0.00')  # Update if needed
    gst = subscription_price * Decimal('0.0')           # Update if needed
    total_amount = subscription_price + service_fee + gst

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=int(total_amount * 100), currency='INR', payment_capture='1'))
    razorpay_order_id = razorpay_order['id']
    
    print("###########################")
    print(razorpay_order)
    print("###########################")

    return render(request, 'payment/payment_page.html', {
        'subscription': subscription,
        'service_fee': service_fee,
        'gst': gst,
        'total_amount': total_amount,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'callback_url': request.build_absolute_uri(reverse('payment_callback'))
    })

@login_required
def payment_callback(request):
    if request.method == 'POST':
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Verify Razorpay payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # Fetch payment details directly from Razorpay
            payment_details = razorpay_client.payment.fetch(razorpay_payment_id)
            amount = Decimal(payment_details['amount']) / 100  # Convert paise to INR


            # Update payment details in the database
            payment, created = Payment.objects.update_or_create(
                razorpay_payment_id=razorpay_payment_id,
                defaults={
                    'recruiter': request.user,
                    'candidate': request.user.profile,
                    'amount': amount,
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_signature': razorpay_signature,
                    'status': 'successful'
                }
            )
            print("Request POST data:", request.POST)


            # Send invoice email
            context = {
                'recruiter': request.user,
                'candidate_name': request.user.profile.preferred_candidate_name,
                'candidate_username': request.user.profile.preferred_candidate_username,
                'amount': amount,
                'payment_method': 'Razorpay',
                'date': payment.payment_date
            }
            subject = 'Payment Confirmation and Invoice'
            html_message = render_to_string('payment/invoice.html', context)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = request.user.email

            msg = EmailMultiAlternatives(subject, html_message, from_email, [to_email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            logger.info("Email sent successfully")

            messages.success(request, 'Payment processed successfully! An invoice has been sent to your email.')
            return redirect('payment_successful')

        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f'Razorpay Signature Verification Error: {e}')
            messages.error(request, 'Payment verification failed. Please try again.')

            # Update payment status to failed
            payment, created = Payment.objects.update_or_create(
                razorpay_payment_id=razorpay_payment_id,
                defaults={
                    'recruiter': request.user,
                    'candidate': request.user.profile,
                    'amount': Decimal(request.POST.get('amount', '0')) / 100,
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_signature': razorpay_signature,
                    'status': 'failed'
                }
            )
            return redirect('payment_failed', error_code='INVALID_SIGNATURE', error_description=str(e))

        except Exception as e:
            logger.error(f'Error processing payment callback: {e}')
            messages.error(request, 'An error occurred while processing the payment. Please try again later.')
            print(f'Error processing payment callback: {e}')

            # Update payment status to failed
            payment, created = Payment.objects.update_or_create(
                razorpay_payment_id=razorpay_payment_id,
                defaults={
                    'recruiter': request.user,
                    'candidate': request.user.profile,
                    'amount': Decimal(request.POST.get('amount', '0')) / 100,
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_signature': razorpay_signature,
                    'status': 'failed'
                }
            )
            return redirect('payment_failed', error_code='UNKNOWN_ERROR', error_description=str(e))


    return HttpResponse("Payment callback received.")


@login_required
def edit_billing_info(request, subscription_id):
    # Fetch or create the profile associated with the current user
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={
        'full_name': '',
        'company_name': '',
        'country': '',
        'state': '',
        'address': '',
        'city': '',
        'postal_code': '',
        'is_indian_citizen': False,
        'receive_invoices_via_email': False
    })
    if request.method == 'POST':
        # Update profile fields based on POST data
        profile.full_name = request.POST.get('full_name', '')
        profile.company_name = request.POST.get('company_name', '')
        profile.country = request.POST.get('country', '')
        profile.state = request.POST.get('state', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.is_indian_citizen = request.POST.get('is_indian_citizen') == 'yes'
        profile.receive_invoices_via_email = 'receive_invoices_via_email' in request.POST
        
        # Save preferred candidate details
        profile.preferred_candidate_name = request.POST.get('preferred_candidate_name', '')
        profile.preferred_candidate_username = request.POST.get('preferred_candidate_username', '')
        profile.save()
        
        # Redirect to payment page with the correct subscription_id
        return redirect('payment_page', subscription_id=subscription_id)

    return render(request, 'payment/edit_billing_info.html', {'profile': profile})

def subscription_list(request):
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        subscription.features_list = subscription.features.split(",")
    return render(request, 'payment/subscription_list.html', {'subscriptions': subscriptions})

def payment_successful(request):
    payment_id = request.GET.get('payment_id')
    print(payment_id)
    return render(request, 'payment/payment_successful.html', {'payment_id': payment_id})

def payment_failed(request):
    error_code = request.GET.get('error_code')
    error_description = request.GET.get('error_description')
    return render(request, 'payment/payment_failed.html', {
        'error_code': error_code,
        'error_description': error_description,
    })
