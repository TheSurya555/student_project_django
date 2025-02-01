from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from studentPost.models import BlogPost
from .models import Service ,Service_page
from profiles.models import UserProfile
from signUp.models import CustomUser

from admin_customization.models import HeroSection, WorkStep, ContactInfo

def services_View(request):
    posts = BlogPost.objects.all()
    services = Service.objects.all()
    service_pages = Service_page.objects.all()
    paginator = Paginator(posts, 8) 
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
        'services': services,
        'service_pages':service_pages
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
                
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None                        

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
  
    social_links = candidate.social_links.all()     
    
    return render(request, 'services/candidate_profile.html', {
        'candidate': candidate,
        'service_id': service_id,
        'profile_image_url': profile_image_url,
        'social_links':social_links,
    })


def all_services(request):
    services = Service.objects.all()
    service_pages = Service_page.objects.all()
    
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
    
    return render(request, 'services/all_services.html', {
        'services': services,
        'profile_image_url': profile_image_url,
        'service_pages':service_pages
    })

def all_candidates(request):
    """View to list all candidates."""
    try:
        # Fetch paginated services
        services = Service.objects.all()
        paginator = Paginator(services, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Fetch other required data
        hero_section = HeroSection.objects.first()
        work_steps = WorkStep.objects.all()
        contact_info = ContactInfo.objects.first()

        profile_image_url = None
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
            except UserProfile.DoesNotExist:
                profile_image_url = None

        # Fetch and sort all candidates by level
        all_candidates = CustomUser.objects.filter(role='candidate',
        tests__score__gt=0 #Ensure they have a score greater than 0                                      
        )
        

        return render(request, 'services/all_candidate_list.html', {
            'profile_image_url': profile_image_url,
            'services': services,
            'page_obj': page_obj,
            'hero_section': hero_section,
            'work_steps': work_steps,
            'contact_info': contact_info,
            'service_pages': Service_page.objects.all(),
            'all_candidates': all_candidates,
        })
    except UnicodeDecodeError:
        return render(request, 'main/error.html', {'error_message': 'UnicodeDecodeError occurred'})
    
def candidate_detail(request, candidate_id):
    """View to display the profile details of a candidate."""
    # Fetch candidate object
    candidate = get_object_or_404(CustomUser, id=candidate_id, role='candidate')

    # Fetch associated user profile, if available
    user_profile = UserProfile.objects.filter(user=candidate).first()

    return render(request, 'services/candidate_detail.html', {
        'candidate': candidate,
        'user_profile': user_profile,
    })    