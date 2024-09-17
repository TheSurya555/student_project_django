# from django.shortcuts import render, get_object_or_404
# from signUp.models import CustomUser
# from services.models import Service
# from profiles.models import UserProfile
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseServerError


# @login_required
# def layout_view(request):
#     try:
#         user_profile = get_object_or_404(UserProfile, user=request.user)
#         profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
#         user_online = request.user.is_online()
#     except UserProfile.DoesNotExist:
#         profile_image_url = None
#         user_online = False

#     return render(request, 'main/Layout.html', {
#         'profile_image_url': profile_image_url,
#         'user_online': user_online,
#     })


# def home_view(request):
#     try:
#         # Fetch users with related recruiter and candidate profiles
#         users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
#         services = Service.objects.all()

#         # Paginate services
#         paginator = Paginator(services, 6)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         # Fetch user profile image if the user is authenticated
#         profile_image_url = None
#         if request.user.is_authenticated:
#             try:
#                 user_profile = UserProfile.objects.get(user=request.user)
#                 profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
#             except UserProfile.DoesNotExist:
#                 profile_image_url = None

#         return render(request, 'main/Index.html', {
#             'users': users,
#             'profile_image_url': profile_image_url,
#             'services': services,
#             'page_obj': page_obj,
#         })

#     except UnicodeDecodeError:
#         return HttpResponseServerError("UnicodeDecodeError occurred while processing the request.")

#     except Exception as e:
#         # Log the exception or handle it as needed
#         return render(request, 'main/error.html', {'error_message': str(e)})


# def custom_404(request, exception):
#     return render(request, '404.html', status=404)


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
        profile_image_url=None 

    user_online = request.user.is_online()

    return render(request, 'main/Layout.html', {
        'profile_image_url': profile_image_url,
        'user_online': user_online,
    })
    
def home_view(request):
    try:
        users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
        services = Service.objects.all()
        paginator = Paginator(services, 6)  # Paginate after fetching services
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        profile_image_url = None
        # Check if the user is authenticated before querying the profile
        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
            except UserProfile.DoesNotExist:
                profile_image_url = None

        return render(request, 'main/Index.html', {
            'users': users,
            'profile_image_url': profile_image_url,
            'services': services,  # Services might not be necessary since you already have page_obj
            'page_obj': page_obj,
        })
    except UnicodeDecodeError:
        return render(request, 'main/error.html', {'error_message': 'UnicodeDecodeError occurred'})
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)