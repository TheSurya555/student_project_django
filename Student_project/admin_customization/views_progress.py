# views.py
from .views import admin_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from progress_tracker.models import Project
from .specific_forms.forms_progress import ProjectAssignmentForm


@login_required
@admin_required
def project_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from GET request
    projects = Project.objects.all()

    # Filter projects based on the search query
    if search_query:
        projects = projects.filter(project_name__icontains=search_query)

    context = {
        'projects': projects,
        'search_query': search_query,  # Pass the search query to the template
    }
    return render(request, 'admin_customization/project_progress/project_list.html', context)

# View to assign project to a candidate
@login_required
@admin_required
def assign_project(request):
    if request.method == 'POST':
        form = ProjectAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project assigned successfully!')
            return redirect('project_list')  # Change to your desired redirect URL
    else:
        form = ProjectAssignmentForm()
    
    return render(request, 'admin_customization/project_progress/assign_project.html', {'form': form})

@login_required
@admin_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectAssignmentForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('project_list')  # Change to your desired redirect URL
    else:
        form = ProjectAssignmentForm(instance=project)
    
    return render(request, 'admin_customization/project_progress/edit_project.html', {'form': form, 'project': project})

@login_required
@admin_required
def project_progress(request, project_id):
    # Retrieve the project based on the provided ID
    project = get_object_or_404(Project, id=project_id)
    
    # Retrieve all progress records related to this project
    progress_records = project.progresses.all()
    
    context = {
        'project': project,
        'progress_records': progress_records
    }
    return render(request, 'admin_customization/project_progress/project_progress.html', context)