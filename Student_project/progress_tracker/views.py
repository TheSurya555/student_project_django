from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Progress
from .forms import ProgressForm, StatusForm
from django.contrib.auth import get_user_model
from notifications.signals import notify
from notifications.models import Notification
from django.db.models import Q
from profiles.models import UserProfile

User = get_user_model()
@login_required
def project_progress_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None

    # Create initial progress records only if they don't exist for the project
    if not Progress.objects.filter(project=project).exists():
        stages = project.get_stages()
        for stage in stages:
            Progress.objects.create(project=project, stage=stage, user=request.user)

    progresses = Progress.objects.filter(project=project)
    cost_per_stage = project.get_cost_per_stage()

    # Check if all progress stages are completed and confirmed
    all_stages_completed = progresses.filter(is_completed=True, client_confirmation=True).count() == progresses.count()

    # Update project status to "completed" if all stages are completed
    if all_stages_completed and project.status != "completed":
        project.status = "completed"
        project.save()

    progress_data = [
        {
            'progress': progress,
            'cost_per_stage': cost_per_stage
        }
        for progress in progresses
    ]

    return render(request, 'progress_tracker/project_progress.html', {
        'project': project,
        'progress_data': progress_data,
        'cost_per_stage': cost_per_stage,
        'profile_image_url': profile_image_url,
        'all_stages_completed': all_stages_completed,
    })

@login_required
def update_progress_view(request, progress_id):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
            
    progress = get_object_or_404(Progress, id=progress_id)
    project = progress.project
    
    # Check if the project is terminated
    if project.status == 'terminated':
        messages.error(request, 'You cannot edit progress for a terminated project.')
        return redirect('project_progress', project_id=project.id)
    
    # Get all progress stages for the project
    stages = list(project.progresses.order_by('id'))
    
    # Find the index of the current progress stage
    current_index = stages.index(progress)
    
    # Check if all previous stages are completed
    if any(not stage.is_completed for stage in stages[:current_index]):
        return render(request, 'progress_tracker/update_progress.html', {
            'form': ProgressForm(instance=progress),
            'progress': progress,
            'error': 'You must complete previous stages before updating this one.',
            'project': project,
        })
    
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user  # Ensure user is set
            progress.save()
            
            # Notify the client about the progress update
            notify.send(
                request.user,
                recipient=project.client,
                verb='Updated progress for project',
                description=f'Progress on stage "{progress.stage}" has been updated.'
            )
            
            # Notify all admins about the progress update
            admin_users = User.objects.filter(is_staff=True)  # Assuming admins are staff users
            for admin in admin_users:
                notify.send(
                    request.user,
                    recipient=admin,
                    verb='Updated progress for project',
                    description=f'Progress on stage "{progress.stage}" for project "{project.project_name}" has been updated.'
                )
            
            messages.success(request, 'Progress updated successfully.')
            return redirect('project_progress', project_id=project.id)
    else:
        form = ProgressForm(instance=progress)
    
    return render(request, 'progress_tracker/update_progress.html', {
        'form': form,
        'progress': progress,
        'project': project,
        'profile_image_url':profile_image_url
    })

@login_required
def update_project_status_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None    
    
    # Check if the user is a recruiter
    if request.user.role != 'recruiter':
        messages.error(request, 'You do not have permission to update the project status.')
        return redirect('project_progress', project_id=project.id)
    
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=project)
        if form.is_valid():
            if form.cleaned_data.get('terminate'):
                project.status = 'terminated'
                project.save()
                
                # Notify all involved users about project termination
                notify.send(
                    request.user,
                    recipient=project.client,
                    verb='Project terminated',
                    description=f'The project "{project.project_name}" has been terminated.'
                )
                
                # Notify all admins about the project termination
                admin_users = User.objects.filter(is_staff=True)  # Assuming admins are staff users
                for admin in admin_users:
                    notify.send(
                        request.user,
                        recipient=admin,
                        verb='Project terminated',
                        description=f'The project "{project.project_name}" has been terminated.'
                    )
                
                messages.success(request, 'Project has been successfully terminated.')
                return redirect('project_progress', project_id=project.id)
            else:
                form.save()
                messages.success(request, 'Project status has been updated.')
                return redirect('project_progress', project_id=project.id)
    else:
        form = StatusForm(instance=project)
    
    return render(request, 'progress_tracker/update_project_status.html', {
        'form': form,
        'project': project,
        'profile_image_url':profile_image_url,
    })

@login_required
def confirm_progress_view(request, progress_id):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    
    progress = get_object_or_404(Progress, id=progress_id)
    project = progress.project
    
    # Check if the user is a recruiter (client)
    if request.user.role != 'recruiter':
        messages.error(request, 'You do not have permission to confirm progress.')
        return redirect('project_progress', project_id=project.id)
    
    # Check if the progress stage is completed
    if not progress.is_completed:
        messages.error(request, 'You cannot confirm an incomplete progress stage.')
        return redirect('project_progress', project_id=project.id)
    
    if request.method == 'POST':
        progress.client_confirmation = True
        progress.save()
        
        # Notify the user who updated the progress about the confirmation
        notify.send(
            request.user,
            recipient=progress.user,
            verb='Progress confirmed',
            description=f'Your progress on stage "{progress.stage}" for the project "{project.project_name}" has been confirmed.'
        )
        
        # Notify all admins about the progress confirmation
        admin_users = User.objects.filter(is_staff=True)  # Assuming admins are staff users
        for admin in admin_users:
            notify.send(
                request.user,
                recipient=admin,
                verb='Progress confirmed',
                description=f'Progress on stage "{progress.stage}" for project "{project.project_name}" has been confirmed.'
            )
        
        messages.success(request, 'Progress stage has been confirmed.')
        return redirect('project_progress', project_id=project.id)
    
    return render(request, 'progress_tracker/confirm_progress.html', {
        'progress': progress,
        'project': project,
        'profile_image_url':profile_image_url
    })
