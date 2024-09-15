from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from services.models import Service
from talents.models import Skills
from examination.models import *
from django.http import HttpResponseForbidden
from .forms import ServiceForm ,SkillForm ,Exam_SkillForm ,QuestionForm

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseForbidden(_("You do not have permission to access this page."))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("Welcome, {}!").format(user.username))
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'site_header': _("TalentSprout Admin Login"),
    }
    return render(request, 'admin_customization/login.html', context)

@login_required    
@admin_required
def dashboard(request):
    return render(request, 'admin_customization/dashboard.html')

@login_required
@admin_required
def profile(request):
    return render(request, 'admin_customization/profile.html')

@login_required
@admin_required
def billing(request):
    return render(request, 'admin_customization/billing.html')

@login_required
@admin_required
def service(request):
    service_obj = Service.objects.all()
    skills_obj = Skills.objects.all()
    
    context ={
        'service_obj':service_obj,
        'skills_obj':skills_obj
    }
    return render(request, 'admin_customization/service.html' ,context)

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
    return render(request, 'admin_customization/edit_service.html', context)

@login_required
@admin_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully!")
            return redirect(reverse('service'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SkillForm()

    context = {
        'form': form,
        'site_header': "Add Skill"
    }
    return render(request, 'admin_customization/add_skill.html', context)


@login_required
@admin_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skills, id=skill_id)
    skill.delete()
    messages.success(request, "Skill deleted successfully!")
    return redirect(reverse('service'))

def admin_logout_view(request):
    logout(request)
    messages.success(request, _("You have successfully logged out."))
    return redirect(reverse('admin_login'))


@login_required
@admin_required
def examination(request):
    skills = Skill.objects.all()
    selected_skill = None
    questions = []

    # Check if a skill has been selected by the admin
    if 'skill_id' in request.GET:
        selected_skill = get_object_or_404(Skill, id=request.GET.get('skill_id'))
        questions = Question.objects.filter(skill=selected_skill)

    context = {
        'skills': skills,
        'selected_skill': selected_skill,
        'questions': questions,
        'site_header': "Manage Examination Skills and Questions"
    }

    return render(request, 'admin_customization/exam/examination.html', context)

@login_required
@admin_required
def exam_add_skill(request):
    if request.method == 'POST':
        form = Exam_SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill added successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Exam_SkillForm()

    context = {
        'form': form,
        'site_header': "Add New Skill"
    }
    return render(request, 'admin_customization/exam/exam_add_skill.html', context)

@login_required
@admin_required
def exam_edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == 'POST':
        form = Exam_SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = Exam_SkillForm(instance=skill)

    context = {
        'form': form,
        'site_header': "Edit Exam Skill"
    }
    return render(request, 'admin_customization/exam/exam_edit_skill.html', context)

@login_required
@admin_required
def exam_delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    messages.success(request, "Skill deleted successfully!")
    return redirect(reverse('examination'))

@login_required
@admin_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            skill_id = request.POST.get('skill')  # Get the selected skill ID from POST data
            skill = get_object_or_404(Skill, id=skill_id)
            question = form.save(commit=False)
            question.skill = skill
            question.save()
            messages.success(request, "Question added successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = QuestionForm()

    context = {
        'form': form,
        'site_header': "Add New Question"
    }
    return render(request, 'admin_customization/exam/add_question.html', context)


@login_required
@admin_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = QuestionForm(instance=question)

    context = {
        'form': form,
        'site_header': "Edit Question"
    }
    return render(request, 'admin_customization/exam/edit_question.html', context)


@login_required
@admin_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "Question deleted successfully!")
    return redirect(reverse('examination'))