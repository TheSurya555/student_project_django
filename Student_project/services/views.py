from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from studentPost.models import BlogPost
from .models import Service
from profiles.models import UserProfile
from signUp.models import CandidateProfile


def services_View(request):
    posts = BlogPost.objects.all()
    services = Service.objects.all()
    paginator = Paginator(posts, 8)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profile_image_url = None
    
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    
    return render(request, 'services/services.html', {
        'page_obj': page_obj,
        'profile_image_url': profile_image_url,
        'services': services
    })


def service_candidates(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    # Improved filtering logic
    service_skills = [skill.strip().lower() for skill in service.skills.split(',')]
    matching_candidates = []
    
    all_candidates = UserProfile.objects.all()
    for candidate in all_candidates:
        if candidate.skills:
            candidate_skills = [skill.strip().lower() for skill in candidate.skills.split(',')]
            if any(skill in candidate_skills for skill in service_skills):
                matching_candidates.append(candidate)
                
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None                        

    return render(request, 'services/candidates.html', {
        'service': service,
        'candidates': matching_candidates,
        'profile_image_url':profile_image_url,
    })


def candidate_profile(request, candidate_id):
    candidate = get_object_or_404(UserProfile, id=candidate_id)
    service_id = request.GET.get('service_id')  # Retrieve the service_id from the query parameters
    profile_image_url = None
    
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    
    return render(request, 'services/candidate_profile.html', {
        'candidate': candidate,
        'service_id': service_id,
        'profile_image_url': profile_image_url
    })


def all_services(request):
    services = Service.objects.all()
    profile_image_url = None
    
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    
    return render(request, 'services/all_services.html', {
        'services': services,
        'profile_image_url': profile_image_url
    })
