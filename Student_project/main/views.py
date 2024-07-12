from django.shortcuts import render
from signUp.models import CustomUser
from services.models import Service
from profiles.models import UserProfile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def layout_View(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    except UserProfile.DoesNotExist:
        profile_image_url = None
    
    user_online = request.user.is_online()

    return render(request, 'main/Layout.html', {
        'profile_image_url': profile_image_url,
        'user_online': user_online,
    })
def home_View(request):
    try:
        users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
        services = Service.objects.all()
        paginator = Paginator(services, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        profile_image_url = None
        return render(request, 'main/Index.html', {
            'users': users,
            'profile_image_url': profile_image_url,
            'services': services,
            'page_obj': page_obj,
        })
    except UnicodeDecodeError as e:
        return render(request, 'main/error.html', {'error_message': 'UnicodeDecodeError occurred'})

def custom_404(request, exception):
    return render(request, '404.html', status=404)