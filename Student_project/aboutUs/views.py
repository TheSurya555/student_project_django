from django.shortcuts import render
from .models import TeamMember

def aboutUs_view(request):
    team_members = TeamMember.objects.all()
    has_team_members = team_members.exists()
    return render(request, 'aboutUs/aboutUs.html', {
        'team_members': team_members,
        'has_team_members': has_team_members,
    })
