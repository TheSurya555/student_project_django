from django.shortcuts import render
from django.core.paginator import Paginator
from studentPost.models import BlogPost
from profiles.models import UserProfile

def services_View(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profile_image_url = None
    return render(request, 'services/services.html', {'page_obj': page_obj, 'profile_image_url': profile_image_url})
