from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Skill, Test, Question, Answer
from datetime import timedelta
from profiles.models import UserProfile

def choose_skill(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    skills = Skill.objects.all()

    return render(request, 'examination/choose_skill.html', {'skills': skills, 'profile_image_url':profile_image_url})

def rules_and_regulations(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        
    return render(request, 'examination/rules_and_regulations.html', {'profile_image_url':profile_image_url})

@login_required
def start_test(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    # Check if the user has completed a test for this skill in the last 10 days
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None    
    recent_test = Test.objects.filter(user=request.user, skill=skill, completed=True).order_by('-completed_date').first()
    if recent_test and recent_test.completed_date and (timezone.now() - recent_test.completed_date).days < 10:
        return render(request, 'examination/cannot_retake_test.html', {'next_attempt_date': recent_test.completed_date + timedelta(days=10) ,'profile_image_url':profile_image_url})
    
    test, created = Test.objects.get_or_create(user=request.user, skill=skill, completed=False)
    return redirect('take_test', test_id=test.id)

@login_required
def take_test(request, test_id):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None    
    test = get_object_or_404(Test, id=test_id, user=request.user)
    questions = test.skill.questions.all()
    
    if request.method == 'POST':
        github_link = request.POST.get('github_link')
        
        if github_link:
            # If GitHub link is provided, save it and mark test as completed
            test.github_link = github_link
            test.completed = True
            test.completed_date = timezone.now()
            test.save()
            return redirect('test_completed', test_id=test.id)
        else:
            # If no GitHub link, process answers for each question
            for question in questions:
                answer_text = request.POST.get(f'question_{question.id}')
                if not answer_text:
                    return render(request, 'examination/take_test.html', {'test': test, 'questions': questions, 'error': 'All questions must be answered.'})
                is_correct = answer_text == question.correct_answer
                Answer.objects.create(
                    test=test,
                    question=question,
                    answer=answer_text,
                    is_correct=is_correct
                )
            
            # Calculate score and mark test as completed
            test.completed = True
            test.completed_date = timezone.now()
            test.score = sum(answer.is_correct for answer in test.answers.all()) / len(questions) * 100
            test.save()
            return redirect('test_completed', test_id=test.id)
    
    return render(request, 'examination/take_test.html', {'test': test, 'questions': questions , 'profile_image_url':profile_image_url})


@login_required
def test_completed(request, test_id):
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None    
    test = get_object_or_404(Test, id=test_id, user=request.user)
    return render(request, 'examination/test_completed.html', {'test': test, 'home_url': '/' ,'profile_image_url':profile_image_url})