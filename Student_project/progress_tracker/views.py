# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Progress
from .forms import ProgressForm, StatusForm

@login_required
def project_progress_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    progresses = Progress.objects.filter(project=project, user=request.user)
    
    if not progresses.exists():
        # Create initial progress records for each stage
        stages = project.get_stages()
        for stage in stages:
            Progress.objects.create(project=project, stage=stage, user=request.user)

    progresses = Progress.objects.filter(project=project, user=request.user)
    cost_per_stage = project.get_cost_per_stage()
    
    # Add cost per stage to each progress item
    progress_data = [
        {
            'progress': progress,
            'cost_per_stage': cost_per_stage
        }
    for progress in progresses]
    
    return render(request, 'progress_tracker/project_progress.html', {
        'project': project,
        'progress_data': progress_data,
        'cost_per_stage': cost_per_stage
    })

@login_required
def update_progress_view(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id, user=request.user)
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
            'project': project
        })
    
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('project_progress', project_id=project.id)
    else:
        form = ProgressForm(instance=progress)
    
    return render(request, 'progress_tracker/update_progress.html', {
        'form': form,
        'progress': progress,
        'project': project
    })

@login_required
def update_project_status_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=project)
        if form.is_valid():
            if form.cleaned_data.get('terminate'):
                # Handle termination
                project.status = 'terminated'
                project.save()
                messages.success(request, 'Project has been successfully terminated.')
                return redirect('project_progress', project_id=project.id)
            else:
                # Handle status update
                form.save()
                messages.success(request, 'Project status has been updated.')
                return redirect('project_progress', project_id=project.id)
    else:
        form = StatusForm(instance=project)
    
    return render(request, 'progress_tracker/update_project_status.html', {
        'form': form,
        'project': project
    })
