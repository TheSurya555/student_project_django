from django.shortcuts import render, get_object_or_404
from services.models import Service
from profiles.models import UserProfile
from .models import Skills
import random
from django.http import JsonResponse

def talent_view(request):
    all_skills = list(Skills.objects.all())
    total_skills = len(all_skills)
    random_skill = random.choice(all_skills)
    related_services = Service.objects.filter(skills__icontains=random_skill.skill)
    related_user_profiles = UserProfile.objects.filter(skills__icontains=random_skill.skill)
    rest_of_skills = Skills.objects.exclude(id=random_skill.id)
    random_contracts = f"{random.randint(10, 50)}+"

    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None

    context = {
        'random_skill': random_skill.skill,
        'related_services': related_services,
        'related_user_profiles': related_user_profiles,
        'rest_of_skills': rest_of_skills,
        'total_skills': total_skills,
        'random_contracts': random_contracts,
        'profile_image_url':profile_image_url
    }

    return render(request, 'talents/talents.html', context)

def fetch_skill_data(request, skill_id):
    skill = Skills.objects.get(id=skill_id)
    related_services = Service.objects.filter(skills__icontains=skill.skill)
    related_user_profiles = UserProfile.objects.filter(skills__icontains=skill.skill)
    random_contracts = f"{random.randint(10, 50)}+"

    data = {
        'random_skill': skill.skill,
        'random_contracts': random_contracts,
        'related_services': [
            {
                'id': service.id,
                'name': service.name,
                'icon': service.icon.url if service.icon else None  # Add the icon URL or None if not available
            } 
            for service in related_services
        ],
        'related_user_profiles': [
            {
                'profile_image': user.profile_image.url,
                'username': user.user.username
            } 
            for user in related_user_profiles
        ],
    }

    return JsonResponse(data)


def skill_service_candidates(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    all_candidates = UserProfile.objects.all()

    service_skills = [skill.strip().lower() for skill in service.skills.split(',')]
    matching_candidates = []

    for candidate in all_candidates:
        if candidate.skills:
            candidate_skills = [skill.strip().lower() for skill in candidate.skills.split(',')]
            if any(skill in candidate_skills for skill in service_skills):
                matching_candidates.append(candidate)

    return render(request, 'services/candidates.html', {'service': service, 'candidates': matching_candidates})
