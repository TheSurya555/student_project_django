from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment, Profile  # Make sure to import the Profile model
from signUp.models import CustomUser  # Adjust the import according to your project structure
from django.contrib import messages
from django.http import JsonResponse

@login_required
def payment_page(request, candidate_id):
    candidate = get_object_or_404(CustomUser, id=candidate_id)
    return render(request, 'payment/payment_page.html', {'candidate': candidate})

@login_required
def process_payment(request):
    if request.method == 'POST':
        upi_id = request.POST.get('upi_id', '')
        card_number = request.POST.get('card_number', '')
        card_expiry = request.POST.get('card_expiry', '')
        card_cvv = request.POST.get('card_cvv', '')
        amount = 100.00  # You can set this dynamically based on your requirement
        
        recruiter = request.user
        candidate = get_object_or_404(CustomUser, username=request.POST['candidate_username'])
        
        # Process the payment here
        # For demonstration purposes, we will assume payment is always successful
        
        # Determine the payment method
        if upi_id:
            payment_method = 'UPI'
        else:
            payment_method = 'Card'
        
        # Save the payment details in the database
        Payment.objects.create(
            recruiter=recruiter,
            candidate=candidate,
            amount=amount,
            payment_method=payment_method
        )
        
        messages.success(request, 'Payment processed successfully!')
        return redirect('success_page')  # Redirect to a success page or any other page
    else:
        messages.error(request, 'Invalid request')
        return redirect('payment_page')
    
# views.py
from django.shortcuts import render

def success_page(request):
    return render(request, 'payment/success.html')
    

@login_required
def edit_billing_info(request):
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
        profile.full_name = request.POST.get('full_name')
        profile.company_name = request.POST.get('company_name')
        profile.country = request.POST.get('country')
        profile.state = request.POST.get('state')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.postal_code = request.POST.get('postal_code')
        profile.is_indian_citizen = request.POST.get('is_indian_citizen') == 'yes'
        profile.receive_invoices_via_email = 'receive_invoices_via_email' in request.POST
        profile.save()
        return redirect('payment_page', candidate_id=request.user.id)  # Redirect to the payment page after saving
    return render(request, 'payment/edit_billing_info.html', {'profile': profile})