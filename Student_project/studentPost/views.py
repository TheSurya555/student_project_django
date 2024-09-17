from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from .forms import BlogPostForm , CandidatePreferenceForm
from .models import BlogPost, CandidatePreference
from profiles.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def studentPost(request):
    posts = BlogPost.objects.filter(user=request.user)
    
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
            
    print('profile_image_url' ,profile_image_url)
    return render(request, 'studentPost/studentPost.html', {'posts': posts ,'user_profile': user_profile ,'profile_image_url': profile_image_url })

def postDetail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    related_posts = BlogPost.objects.filter(user=post.user).exclude(id=post.id)[:3]

    user_profile = None
    profile_image_url = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=post.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            user_profile = None
            profile_image_url = None

    # Fetch candidate preference related to the post
    try:
        candidate_preference = CandidatePreference.objects.get(blog_post=post)
    except CandidatePreference.DoesNotExist:
        candidate_preference = None

    return render(request, 'studentPost/postdetailes.html', {
        'post': post,
        'user_profile': user_profile,
        'related_posts': related_posts,
        'profile_image_url': profile_image_url,
        'candidate_preference': candidate_preference  # Pass candidate preference to the template
    })


@login_required
def create_blog_post(request):
    if request.method == 'POST':
        blog_post_form = BlogPostForm(request.POST, request.FILES)
        candidate_preference_form = CandidatePreferenceForm(request.POST)
        
        if blog_post_form.is_valid() and candidate_preference_form.is_valid():
            blog_post = blog_post_form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()

            # Create a CandidatePreference based on form data
            candidate_preference = candidate_preference_form.save(commit=False)
            candidate_preference.blog_post = blog_post
            candidate_preference.save()

            return redirect('studentpost')  # Redirect to the blog list page
    else:
        blog_post_form = BlogPostForm()
        candidate_preference_form = CandidatePreferenceForm()

    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            pass    

    return render(request, 'studentPost/post_creation_form.html', {
        'blog_post_form': blog_post_form,
        'candidate_preference_form': candidate_preference_form,
        'profile_image_url':profile_image_url,
    })
