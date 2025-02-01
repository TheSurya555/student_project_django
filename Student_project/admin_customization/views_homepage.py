from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .specific_forms.forms_homepage import *
from .views import admin_required
from django.forms import modelformset_factory

# A common header for all the admin pages
SITE_HEADER = "Admin Dashboard"

@login_required    
@admin_required
def admin_home_page(request):
    hero_sections = HeroSection.objects.all()
    work_steps = WorkStep.objects.all()
    contact_info = ContactInfo.objects.first()

    context = {
        'site_header': "Homepage Management",  # Custom site header for this view
        'hero_sections': hero_sections,
        'work_steps': work_steps,
        'contact_info': contact_info
    }
    
    return render(request, 'admin_customization/homepage/homepage_admin.html', context)


@login_required    
@admin_required
def add_hero_section(request):
    if request.method == 'POST':
        form = HeroSectionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_home_page'))
    else:
        form = HeroSectionForm()

    context = {
        'site_header': "Add Hero Section Content",  # General admin header
        'form': form
    }
    
    return render(request, 'admin_customization/homepage/add_hero_section.html', context)


@login_required    
@admin_required
def edit_hero_section(request, id):
    hero_section = get_object_or_404(HeroSection, id=id)
    if request.method == 'POST':
        form = HeroSectionForm(request.POST, request.FILES, instance=hero_section)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_home_page'))
    else:
        form = HeroSectionForm(instance=hero_section)

    context = {
        'site_header': "Edit Hero Section Content",  # General admin header
        'form': form
    }

    return render(request, 'admin_customization/homepage/edit_hero_section.html', context)


@login_required    
@admin_required
def add_work_step(request):
    if request.method == 'POST':
        form = WorkStepForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_home_page'))
    else:
        form = WorkStepForm()

    context = {
        'site_header': "Add How We Work Steps",  # General admin header
        'form': form
    }
    
    return render(request, 'admin_customization/homepage/add_work_step.html', context)


@login_required    
@admin_required
def edit_work_step(request, id):
    work_step = get_object_or_404(WorkStep, id=id)
    if request.method == 'POST':
        form = WorkStepForm(request.POST, instance=work_step)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_home_page'))
    else:
        form = WorkStepForm(instance=work_step)

    context = {
        'site_header': "Edit How We Work Steps",  # General admin header
        'form': form
    }
    
    return render(request, 'admin_customization/homepage/edit_work_step.html', context)


@login_required    
@admin_required
def add_contact_info(request):
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, request.FILES)  # Ensure to include request.FILES
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_home_page'))
    else:
        form = ContactInfoForm()

    context = {
        'site_header': "Add Contact Information",  # General admin header
        'form': form
    }
    
    return render(request, 'admin_customization/homepage/add_contact_info.html', context)


@login_required    
@admin_required
def edit_contact_info(request, id):
    contact_info = get_object_or_404(ContactInfo, id=id)
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, request.FILES, instance=contact_info)  # Include request.FILES here
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_home_page'))
    else:
        form = ContactInfoForm(instance=contact_info)

    context = {
        'site_header': "Edit Contact Information",  # General admin header
        'form': form
    }
    
    return render(request, 'admin_customization/homepage/edit_contact_info.html', context)




# Delete Hero Section
@login_required    
@admin_required
def delete_hero_section(request, id):
    hero_section = get_object_or_404(HeroSection, id=id)
    if request.method == 'POST':
        hero_section.delete()
        messages.success(request, 'Hero Section deleted successfully!')
        return redirect(reverse('admin_home_page'))

# Delete Work Step
@login_required    
@admin_required
def delete_work_step(request, id):
    work_step = get_object_or_404(WorkStep, id=id)
    if request.method == 'POST':
        work_step.delete()
        messages.success(request, 'Work Step deleted successfully!')
        return redirect(reverse('admin_home_page'))

# Delete Contact Info
@login_required    
@admin_required
def delete_contact_info(request, id):
    contact_info = get_object_or_404(ContactInfo, id=id)
    if request.method == 'POST':
        contact_info.delete()
        messages.success(request, 'Contact Info deleted successfully!')
        return redirect(reverse('admin_home_page'))

@login_required    
@admin_required
def add_footer(request):
    if request.method == 'POST':
        form = FooterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer content added successfully!')
            return redirect(reverse('admin_home_page'))
    else:
        form = FooterForm()

    context = {
        'site_header': "Add Footer Content",  # General admin header
        'form': form
    }

    return render(request, 'admin_customization/homepage/add_footer.html', context)


@login_required    
@admin_required
def edit_footer(request, id):
    footer = get_object_or_404(Footer, id=id)
    if request.method == 'POST':
        form = FooterForm(request.POST, instance=footer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Footer content updated successfully!')
            return redirect(reverse('admin_home_page'))
    else:
        form = FooterForm(instance=footer)

    context = {
        'site_header': "Edit Footer Content",  # General admin header
        'form': form
    }

    return render(request, 'admin_customization/homepage/edit_footer.html', context)


@login_required    
@admin_required
def delete_footer(request, id):
    footer = get_object_or_404(Footer, id=id)
    if request.method == 'POST':
        footer.delete()
        messages.success(request, 'Footer content deleted successfully!')
        return redirect(reverse('admin_home_page'))


@login_required
@admin_required
def add_footer_portfolio_image(request, footer_id):
    footer = get_object_or_404(Footer, id=footer_id)
    if request.method == 'POST':
        form = FooterPortfolioImageForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_image = form.save(commit=False)
            portfolio_image.footer = footer  # Associate the image with the specific footer
            portfolio_image.save()
            messages.success(request, 'Portfolio image added successfully!')
            return redirect(reverse('edit_footer', args=[footer_id]))
    else:
        form = FooterPortfolioImageForm()

    context = {
        'site_header': "Add Portfolio Image",
        'form': form,
        'footer': footer,
    }

    return render(request, 'admin_customization/homepage/add_footer_portfolio_image.html', context)


@login_required
@admin_required
def edit_footer_portfolio_image(request, footer_id, image_id):
    footer = get_object_or_404(Footer, id=footer_id)
    portfolio_image = get_object_or_404(FooterPortfolioImage, id=image_id, footer=footer)
    if request.method == 'POST':
        form = FooterPortfolioImageForm(request.POST, request.FILES, instance=portfolio_image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio image updated successfully!')
            return redirect(reverse('edit_footer', args=[footer_id]))
    else:
        form = FooterPortfolioImageForm(instance=portfolio_image)

    context = {
        'site_header': "Edit Portfolio Image",
        'form': form,
        'footer': footer,
    }

    return render(request, 'admin_customization/homepage/edit_footer_portfolio_image.html', context)


@login_required
@admin_required
def delete_footer_portfolio_image(request, footer_id, image_id):
    footer = get_object_or_404(Footer, id=footer_id)
    portfolio_image = get_object_or_404(FooterPortfolioImage, id=image_id, footer=footer)
    if request.method == 'POST':
        portfolio_image.delete()
        messages.success(request, 'Portfolio image deleted successfully!')
        return redirect(reverse('edit_footer', args=[footer_id]))

    context = {
        'site_header': "Delete Portfolio Image",
        'footer': footer,
        'portfolio_image': portfolio_image,
    }

    return render(request, 'admin_customization/homepage/delete_footer_portfolio_image.html', context)


@login_required
@admin_required
def manage_footer_portfolio_images(request, footer_id):
    footer = get_object_or_404(Footer, id=footer_id)
    PortfolioImageFormSet = modelformset_factory(
        FooterPortfolioImage,
        form=FooterPortfolioImageForm,
        extra=0,
        can_delete=True,
    )
    if request.method == 'POST':
        formset = PortfolioImageFormSet(request.POST, request.FILES, queryset=footer.portfolio_images.all())
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Portfolio images updated successfully!')
            return redirect(reverse('edit_footer', args=[footer_id]))
    else:
        formset = PortfolioImageFormSet(queryset=footer.portfolio_images.all())

    context = {
        'site_header': "Manage Portfolio Images",
        'footer': footer,
        'formset': formset,
    }

    return render(request, 'admin_customization/homepage/manage_footer_portfolio_images.html', context)