from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment, Profile  # Make sure to import the Profile model
from signUp.models import CustomUser  # Adjust the import according to your project structure
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail ,EmailMultiAlternatives
from smtplib import SMTPAuthenticationError, SMTPException
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Subscription
import logging
from decimal import Decimal 

@login_required
def payment_page(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Convert subscription price to Decimal if necessary (depending on your model definition)
    subscription_price = Decimal(subscription.price)
    
    # Calculate service fee and GST based on subscription price (using Decimal)
    service_fee = subscription_price * Decimal('0.02')
    gst = subscription_price * Decimal('0.12')
    total_amount = subscription_price + service_fee + gst
    
    return render(request, 'payment/payment_page.html', {
        'subscription': subscription,
        'service_fee': service_fee,
        'gst': gst,
        'total_amount': total_amount,
    })


logger = logging.getLogger(__name__)

@login_required
def process_payment(request , subscription_id):
    if request.method == 'POST':
        try:
            # Retrieve form data
            upi_id = request.POST.get('upi_id', '')
            card_number = request.POST.get('card_number', '')
            card_expiry = request.POST.get('card_expiry', '')
            card_cvv = request.POST.get('card_cvv', '')

            # Fetch subscription details
            subscription = get_object_or_404(Subscription, id=subscription_id)
            subscription_price = Decimal(subscription.price)

            # Calculate total amount including service fee and GST
            service_fee = subscription_price * Decimal('0.02')
            gst = subscription_price * Decimal('0.12')
            total_amount = subscription_price + service_fee + gst

            # Determine the payment method
            payment_method = 'UPI' if upi_id else 'Card'

            # Save the payment details in the database
            Payment.objects.create(
                recruiter=request.user,
                candidate=request.user.profile,
                amount=total_amount,
                payment_method=payment_method
            )

            # Send invoice email
            context = {
                'recruiter': request.user,
                'candidate_name': request.user.profile.preferred_candidate_name,
                'candidate_username': request.user.profile.preferred_candidate_username,
                'amount': total_amount,
                'payment_method': payment_method,
                'date': timezone.now()
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
            return redirect('success_page')  # Redirect to a success page or any other page

        except SMTPAuthenticationError as e:
            logger.error(f'SMTP Authentication Error: {e}')
            messages.error(request, 'Failed to send email due to authentication error. Please check your email settings.')
            return redirect('payment_page', subscription_id=subscription_id)

        except Exception as e:
            logger.error(f'Error processing payment: {e}')
            messages.error(request, 'An error occurred while processing your payment. Please try again later.')
            return redirect('payment_page', subscription_id=subscription_id)
    else:
        messages.error(request, 'Invalid request')

    # Handle case where redirection is needed but subscription_id is None
    return redirect('payment_page', subscription_id=subscription_id)


def success_page(request):
    return render(request, 'payment/success.html')
    

@login_required
def edit_billing_info(request ,subscription_id):
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
        
        # Retrieve the subscription associated with the user's profile
        subscription = get_object_or_404(Subscription, id=subscription_id)  # Adjust this based on your model structure
        
        print("subscription.id" ,subscription.id)
        # Redirect to payment page with the correct subscription_id
        return redirect('payment_page', subscription_id=subscription.id)

    return render(request, 'payment/edit_billing_info.html', {'profile': profile})


def subscription_list(request):
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        subscription.features_list = subscription.features.split(",")
    return render(request, 'payment/subscription_list.html', {'subscriptions': subscriptions})
