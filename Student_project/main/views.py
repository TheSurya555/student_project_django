from django.shortcuts import render
from signUp.models import CustomUser

# Create your views here.
def layout_View(request):
    return render(request,'main/Layout.html')


def home_View(request):
    users = CustomUser.objects.select_related('recruiter_profile', 'candidate_profile').all()
    profile_image_url = None
    print(profile_image_url)
    print(users)
    return render(request,'main/Index.html' ,{'users':users ,'profile_image_url': profile_image_url})