from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Skill, Test, Answer ,ExamRule
from datetime import timedelta
from profiles.models import UserProfile

def test(request):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    return render(request, 'examination/test.html', {'profile_image_url':profile_image_url})

def choose_skill(request):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    skills = Skill.objects.all()

    return render(request, 'examination/choose_skill.html', {'skills': skills, 'profile_image_url':profile_image_url})

def rules_and_regulations(request):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
            
    rules = ExamRule.objects.all()        
    context = {
        'rules': rules,
        'profile_image_url':profile_image_url,
        'site_header': "Examination Rules and Regulations"
    }
    return render(request, 'examination/rules_and_regulations.html', context)

@login_required
def start_test(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    # Check if the user has completed a test for this skill in the last 10 days
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
   
    recent_test = Test.objects.filter(user=request.user, skill=skill, completed=True).order_by('-completed_date').first()
    if recent_test and recent_test.completed_date and (timezone.now() - recent_test.completed_date).days < 10:
        return render(request, 'examination/cannot_retake_test.html', {'next_attempt_date': recent_test.completed_date + timedelta(days=10) ,'profile_image_url':profile_image_url})
    
    test, created = Test.objects.get_or_create(user=request.user, skill=skill, completed=False)
    return redirect('take_test', test_id=test.id)


@login_required
def take_test(request, test_id):
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None 
            
    test = get_object_or_404(Test, id=test_id, user=request.user)
    questions = test.skill.questions.all()
    
    for question in questions:
        if question.type == 'MCQ' and isinstance(question.options, list):
            question.options_list = question.options

    user_answers = {answer.question_id: answer.answer for answer in test.answers.all()}

    # Initialize error variable
    error = None    
    
    if request.method == 'POST':
        print("Processing POST request")
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}')
            print(f"Question {question.id}: Answer - {answer_text}")
            if not answer_text:
                error = 'All questions must be answered.'
                break
            is_correct = answer_text.strip().lower() == question.correct_answer.strip().lower()
            Answer.objects.update_or_create(
                test=test,
                question=question,
                defaults={'answer': answer_text, 'is_correct': is_correct}
            )

        if not error:
            test.completed = True
            test.completed_date = timezone.now()
            test.save()
            print(f"Redirecting to test_completed with test_id: {test.id}")
            return redirect('test_completed', test_id=test.id)

    return render(request, 'examination/take_test.html', {
        'test': test,
        'questions': questions,
        'profile_image_url': profile_image_url,
        'user_answers': user_answers,
        'error': error
    })

@login_required
def test_completed(request, test_id):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None    
    test = get_object_or_404(Test, id=test_id, user=request.user)
    return render(request, 'examination/test_completed.html', {'test': test, 'home_url': '/' ,'profile_image_url':profile_image_url})