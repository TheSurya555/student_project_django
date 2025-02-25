from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from talents.models import Skills
from examination.models import Skill, Question, Test, Answer,Score
from django.http import HttpResponseForbidden
from .forms import SkillForm ,Exam_SkillForm, QuestionForm,AnswerCorrectionForm,ScoreForm,ExamRulesForm
from django.http import JsonResponse
from notifications.models import Notification
from examination.models import ExamRule
from django.http import HttpResponse

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


# Admin Examination view start

@login_required
@admin_required
def examination(request):
    skills = Skill.objects.all()
    selected_skill = None
    questions = []
    student_tests = Test.objects.all()
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    rules = ExamRule.objects.all()

    # Check if a skill has been selected by the admin
    if 'skill_id' in request.GET:
        selected_skill = get_object_or_404(Skill, id=request.GET.get('skill_id'))
        questions = Question.objects.filter(skill=selected_skill)

    context = {
        'skills': skills,
        'selected_skill': selected_skill,
        'questions': questions,
        'student_tests': student_tests,
        'notifications':notifications,
        'rules': rules,
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
            form.save()
            messages.success(request, "Question added successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, f"Form submission failed: {form.errors}")
    else:
        form = QuestionForm()

    context = {'form': form, 'site_header': "Add New Question"}
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
            messages.error(request, f"Form submission failed: {form.errors}")
    else:
        form = QuestionForm(instance=question)

    context = {'form': form, 'site_header': "Edit Question"}
    return render(request, 'admin_customization/exam/edit_question.html', context)

@login_required
@admin_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "Question deleted successfully!")
    return redirect(reverse('examination'))

@login_required
@admin_required
def view_student_test(request, user_id):
    student_tests = Test.objects.filter(user_id=user_id).prefetch_related('answers')

    # If no tests found, render a no tests page
    if not student_tests.exists():
        return render(request, 'admin_customization/exam/no_test_found.html', {'user_id': user_id})

    if request.method == 'POST':
        test = student_tests[0] 
        # Loop through answers and update scores and correctness
        for answer in test.answers.all():
            answer_id = str(answer.id)  # Assuming the first test for simplicity
            score_value = request.POST.get(f'scores_{answer_id}')
            is_correct = request.POST.get(f'is_correct_{answer_id}')
             
            # Update score for code-based questions
            if score_value:
                score,created = Score.objects.get_or_create(answer=answer)

                if created:
                    # Action when a new score is created
                    print(f"New score created for answer {answer.id}")
                else:
                    # Action when the score already existed
                    print(f"Score already exists for answer {answer.id}")
                score.value = float(score_value)
                score.save()
            
            # Update is_correct for MCQ-based questions
            if is_correct is not None:
                answer.is_correct = is_correct == 'True'
                answer.save()

        # Recalculate the total score for the test
        # Assuming one test per student for simplicity


        test.calculate_total_score()  # This function will sum up the individual scores and update the test

        # Redirect to the examination page after successful updates
        return JsonResponse({'success': True, 'redirect_url': reverse('examination')})

    # Context for rendering the template
    context = {
        'student_tests': student_tests,
        'site_header': f"Tests Details for User: {student_tests[0].user.username}" if student_tests else "No Tests Found",
    }

    return render(request, 'admin_customization/exam/view_student_test.html', context)


@login_required
@admin_required
def delete_student_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    test.delete()
    messages.success(request, "Student's test deleted successfully!")
    return redirect(reverse('examination'))



# Admin examination view end

# Admin view to add a new exam rule
@login_required
@admin_required
def add_exam_rule(request):
    if request.method == 'POST':
        form = ExamRulesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rule added successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExamRulesForm()

    context = {
        'form': form,
        'site_header': "Add New Exam Rule"
    }
    return render(request, 'admin_customization/exam/add_exam_rule.html', context)


# Admin view to edit an exam rule
@login_required
@admin_required
def edit_exam_rule(request, rule_id):
    rule = get_object_or_404(ExamRule, id=rule_id)

    if request.method == 'POST':
        form = ExamRulesForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            messages.success(request, "Rule updated successfully!")
            return redirect(reverse('examination'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExamRulesForm(instance=rule)

    context = {
        'form': form,
        'site_header': "Edit Exam Rule"
    }
    return render(request, 'admin_customization/exam/edit_exam_rule.html', context)


# Admin view to delete an exam rule
@login_required
@admin_required
def delete_exam_rule(request, rule_id):
    rule = get_object_or_404(ExamRule, id=rule_id)
    rule.delete()
    messages.success(request, "Rule deleted successfully!")
    return redirect(reverse('examination'))


@login_required
@admin_required
def update_test_score(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('view_student_test', user_id=test.user.id)
        return HttpResponse('Invalid form submission', status=400)
    return HttpResponse('Invalid request method', status=400)


# Admin logout view start
def admin_logout_view(request):
    logout(request)
    messages.success(request, _("You have successfully logged out."))
    return redirect(reverse('admin_login'))
# Admin logout view end