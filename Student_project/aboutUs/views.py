from django.shortcuts import render
from profiles.models import UserProfile
from .models import TeamMember, AboutUsContent

def aboutUs_view(request):
    try:
        about_us_content = AboutUsContent.objects.latest('created_at')
    except AboutUsContent.DoesNotExist:
        about_us_content = None

    team_members = TeamMember.objects.all()
    has_team_members = team_members.exists()
    
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None

    return render(request, 'aboutUs/aboutUs.html', {
        'about_us_content': about_us_content,
        'team_members': team_members,
        'has_team_members': has_team_members,
        'profile_image_url': profile_image_url
    })
