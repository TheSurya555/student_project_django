from .views import admin_required
from payment.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator
from notifications.models import Notification



class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)

@login_required
@admin_required
def billing(request):
    profiles = Profile.objects.all().order_by('-id')
    paginator = Paginator(profiles, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    payments = Payment.objects.all()
    subscriptions = Subscription.objects.all()
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    # Date filter form
    
    date_filter_form = DateFilterForm(request.GET or None)
    if date_filter_form.is_valid():
        start_date = date_filter_form.cleaned_data.get('start_date')
        end_date = date_filter_form.cleaned_data.get('end_date')
        if start_date:
            payments = payments.filter(payment_date__gte=start_date)
        if end_date:
            payments = payments.filter(payment_date__lte=end_date)
            
    total_amount = sum(payment.amount for payment in payments)    
    
    context ={
        'payments' : payments,
        'subscriptions' : subscriptions,
        'date_filter_form': date_filter_form,
        'page_obj': page_obj,
        'total_amount': total_amount,
        'notifications': notifications,
    }
    
    return render(request, 'admin_customization/Billing/billing.html' , context)


@login_required
@admin_required
def add_subscription_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription added successfully!')
            return redirect('billing')
    else:
        form = SubscriptionForm()
    return render(request, 'admin_customization/Billing/add_subscription.html', {'form': form, 'action': 'Add'})


@login_required
@admin_required
def edit_subscription_view(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription updated successfully!')
            return redirect('billing')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'admin_customization/Billing/edit_subscription.html', {'form': form, 'action': 'Edit'})


@login_required
@admin_required
def delete_subscription_view(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    subscription.delete()
    messages.success(request, 'Subscription deleted successfully!')
    return redirect('billing')


@login_required
@admin_required
def profile_pdf(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    template = get_template('admin_customization/Billing/profile_pdf_template.html')
    context = {'profile': profile}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Profile_{profile.full_name}.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response


@login_required
@admin_required
def payment_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    template = get_template('admin_customization/Billing/payment_pdf_template.html')
    context = {'payment': payment}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Payment_{payment.recruiter}_{payment.id}.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response