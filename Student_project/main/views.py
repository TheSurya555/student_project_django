from django.shortcuts import render
from signUp.models import CustomUser
from services.models import Service, Service_page
from profiles.models import UserProfile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from admin_customization.models import HeroSection, WorkStep, ContactInfo

@login_required
def layout_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    except UserProfile.DoesNotExist:
        profile_image_url=None 

    user_online = request.user.is_online()

    return render(request, 'main/Layout.html', {
        'profile_image_url': profile_image_url,
        'user_online': user_online,
    })
    
def home_view(request):
    try:
        # users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
        users = (
        UserProfile.objects.filter(user__role=CustomUser.CANDIDATE)
        .select_related('user').order_by('-level')[:5]
        )
        
        # Transform users into a list of dictionaries for easy use in the template
        user_data = [
             {
                 'id': user.user.id,
                 'candidate_id': user.id,
                 'first_name': user.user.first_name,
                 'last_name': user.user.last_name,
                 'profile_image': user.profile_image.url if user.profile_image else None,
                 'career_objective': user.career_objective if user.career_objective else "No career objective provided.",
                 **({'level': user.level} if user.level else {})
             }
                for user in users
                    ]
        
        services = Service.objects.all()
        paginator = Paginator(services, 6)  # Paginate after fetching services
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        service_pages = Service_page.objects.all()

        # Fetch HeroSection, WorkStep, and ContactInfo
        hero_section = HeroSection.objects.first()
        work_steps = WorkStep.objects.all()
        contact_info = ContactInfo.objects.first()
        
        profile_image_url = None
        # Check if the user is authenticated before querying the profile
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
            except UserProfile.DoesNotExist:
                profile_image_url = None

        return render(request, 'main/Index.html', {
            # 'users': users,
            'users': user_data,
            'profile_image_url': profile_image_url,
            'services': services,  # Services might not be necessary since you already have page_obj
            'page_obj': page_obj,
            'hero_section': hero_section,
            'work_steps': work_steps,
            'contact_info': contact_info,
            'service_pages':service_pages
        })
    except UnicodeDecodeError:
        return render(request, 'main/error.html', {'error_message': 'UnicodeDecodeError occurred'})


def custom_404(request, exception):
    return render(request, '404.html', status=404)