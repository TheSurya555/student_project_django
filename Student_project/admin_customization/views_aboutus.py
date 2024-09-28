from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from .specific_forms.forms_aboutus import *
from .views import admin_required
from aboutUs.models import *
from contactus.models import *
from profiles.models import *
from notifications.models import Notification

# Admin aboutus view start@login_required
@admin_required
def admin_aboutus_view(request):
    # Fetch all About Us, Features, and Team Members
    about_us_content = AboutUsContent.objects.all()
    features = Feature.objects.all()
    team_members = TeamMember.objects.all()
    support_info_list = SupportInfo.objects.all()
    Privacy_Policy = PrivacyPolicy.objects.all()
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    

    context = {
        'about_us_content': about_us_content,
        'features': features,
        'team_members': team_members,
        'support_info_list': support_info_list,
        'Privacy_Policy':Privacy_Policy,
        'site_header': "Manage About Us, Features, and Team Members",
        'notifications': notifications,
    }
    return render(request, 'admin_customization/aboutus/aboutus.html', context)

@login_required
@admin_required
def add_aboutus_content(request):
    if request.method == 'POST':
        form = AboutUsContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "About Us content added successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AboutUsContentForm()

    return render(request, 'admin_customization/aboutus/add_aboutus.html', {'form': form, 'site_header': "Add About Us Content"})

@login_required
@admin_required
def edit_aboutus_content(request, content_id):
    about_us = get_object_or_404(AboutUsContent, id=content_id)
    
    if request.method == 'POST':
        form = AboutUsContentForm(request.POST, request.FILES, instance=about_us)
        if form.is_valid():
            form.save()
            messages.success(request, "About Us content updated successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AboutUsContentForm(instance=about_us)

    return render(request, 'admin_customization/aboutus/edit_aboutus.html', {'form': form, 'site_header': "Edit About Us Content"})

@login_required
@admin_required
def delete_aboutus_content(request, content_id):
    about_us = get_object_or_404(AboutUsContent, id=content_id)
    about_us.delete()
    messages.success(request, "About Us content deleted successfully!")
    return redirect('admin_aboutus')


@login_required
@admin_required
def add_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Feature added successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeatureForm()

    return render(request, 'admin_customization/aboutus/add_feature.html', {'form': form, 'site_header': "Add Feature"})

@login_required
@admin_required
def edit_feature(request, feature_id):
    feature = get_object_or_404(Feature, id=feature_id)
    
    if request.method == 'POST':
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, "Feature updated successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeatureForm(instance=feature)

    return render(request, 'admin_customization/aboutus/edit_feature.html', {'form': form, 'site_header': "Edit Feature"})

@login_required
@admin_required
def delete_feature(request, feature_id):
    feature = get_object_or_404(Feature, id=feature_id)
    feature.delete()
    messages.success(request, "Feature deleted successfully!")
    return redirect('admin_aboutus')


@login_required
@admin_required
def add_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member added successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamMemberForm()

    return render(request, 'admin_customization/aboutus/add_team_member.html', {'form': form, 'site_header': "Add Team Member"})

@login_required
@admin_required
def edit_team_member(request, member_id):
    team_member = get_object_or_404(TeamMember, id=member_id)

    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member updated successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamMemberForm(instance=team_member)

    return render(request, 'admin_customization/aboutus/edit_team_member.html', {'form': form, 'site_header': "Edit Team Member"})

@login_required
@admin_required
def delete_team_member(request, member_id):
    team_member = get_object_or_404(TeamMember, id=member_id)
    team_member.delete()
    messages.success(request, "Team member deleted successfully!")
    return redirect('admin_aboutus')


# Support Info CRUD Views

@login_required
@admin_required
def add_support_info(request):
    if request.method == 'POST':
        form = SupportInfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Support information added successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SupportInfoForm()

    return render(request, 'admin_customization/aboutus/add_support_info.html', {'form': form, 'site_header': "Add Support Info"})

@login_required
@admin_required
def edit_support_info(request, info_id):
    support_info = get_object_or_404(SupportInfo, id=info_id)

    if request.method == 'POST':
        form = SupportInfoForm(request.POST, request.FILES, instance=support_info)
        if form.is_valid():
            form.save()
            messages.success(request, "Support information updated successfully!")
            return redirect('admin_aboutus')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SupportInfoForm(instance=support_info)

    return render(request, 'admin_customization/aboutus/edit_support_info.html', {'form': form, 'site_header': "Edit Support Info"})

@login_required
@admin_required
def delete_support_info(request, info_id):
    support_info = get_object_or_404(SupportInfo, id=info_id)
    support_info.delete()
    messages.success(request, "Support information deleted successfully!")
    return redirect('admin_aboutus')


# privacy policy 
@login_required
@admin_required
def add_privacy_policy_content(request):
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_aboutus'))  # Replace with the name of your listing URL
    else:
        form = PrivacyPolicyForm()
    
    return render(request, 'admin_customization/aboutus/add_privacy_policy_content.html', {'form': form ,'site_header': "Add Privacy Policy"})

@login_required
@admin_required
def edit_privacy_policy_content(request, pk):
    content = get_object_or_404(PrivacyPolicy, pk=pk)
    
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_aboutus'))  # Replace with the correct URL name
    else:
        form = PrivacyPolicyForm(instance=content)
    
    return render(request, 'admin_customization/aboutus/edit_privacy_policy_content.html', {'form': form ,'site_header': "Edit Privacy Policy"})

@login_required
@admin_required
def delete_privacy_policy_content(request, pk):
    content = get_object_or_404(PrivacyPolicy, id=pk)
    content.delete()
    messages.success(request, "Privacy policy deleted successfully!")
    return redirect('admin_aboutus')