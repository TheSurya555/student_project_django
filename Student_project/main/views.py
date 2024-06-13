from django.shortcuts import render
from signUp.models import CustomUser
from services.models import Service
from django.core.paginator import Paginator

# Create your views here.
def layout_View(request):
    profile_image_url = None
    if request.user.is_authenticated:
        profile_image_url = request.user.profile_image.url if request.user.profile_image else None
        print('profile_image_url' ,profile_image_url)

    return render(request, 'main/Layout.html', {
        'profile_image_url': profile_image_url
    })


def home_View(request):
    users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
    services = Service.objects.all()
    paginator = Paginator(services, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profile_image_url = None
    return render(request,'main/Index.html' ,{'users':users ,'profile_image_url': profile_image_url ,'services': services ,'page_obj': page_obj})


