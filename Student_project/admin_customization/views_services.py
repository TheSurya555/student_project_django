from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from services.models import Service ,Service_page
from .views import admin_required
from .specific_forms.forms_services import *
from .forms import *
from notifications.models import Notification

@login_required
@admin_required
def service(request):
    service_obj = Service.objects.all()
    skills_obj = Skills.objects.all()
    service_pages = Service_page.objects.all() 
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    
    
    context ={
        'service_obj':service_obj,
        'skills_obj':skills_obj,
        'service_pages': service_pages,
        'notifications':notifications,
    }
    return render(request, 'admin_customization/services/service.html' ,context)

@login_required
@admin_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully!")
            return redirect(reverse('service'))  # Redirect to the service list or another page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceForm()

    context = {
        'form': form,
        'site_header': "Add Service"
    }
    return render(request, 'admin_customization/services/add_service.html', context)


@login_required
@admin_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect(reverse('service'))  # Redirect to the service list or another page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceForm(instance=service)

    context = {
        'form': form,
        'service': service,
        'site_header': "Edit Service"
    }
    return render(request, 'admin_customization/services/edit_service.html', context)

@login_required
@admin_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('service')

@login_required
@admin_required
def add_service_page(request):
    if request.method == 'POST':
        form = ServicePageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Page added successfully!")
            return redirect(reverse('service'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServicePageForm()

    context = {
        'form': form,
        'site_header': "Add",
        'action': "Add"
    }
    return render(request, 'admin_customization/services/add_service_page.html', context)


@login_required
@admin_required
def edit_service_page(request, page_id):
    service_page = get_object_or_404(Service_page, id=page_id)

    if request.method == 'POST':
        form = ServicePageForm(request.POST, request.FILES, instance=service_page)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Page updated successfully!")
            return redirect(reverse('service'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServicePageForm(instance=service_page)

    context = {
        'form': form,
        'service_page': service_page,
        'site_header': "Edit",
        'action': "Edit"
    }
    return render(request, 'admin_customization/services/edit_service_page.html', context)


@login_required
@admin_required
def delete_service_page(request, page_id):
    service_page = get_object_or_404(Service_page, id=page_id)
    service_page.delete()
    messages.success(request, "Service Page deleted successfully!")
    return redirect(reverse('service'))

