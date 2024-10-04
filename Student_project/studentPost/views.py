from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import BlogPostForm, CandidatePreferenceForm, BlogImageForm
from .models import BlogPost, CandidatePreference, BlogImage
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
@login_required
def studentPost(request):
    # Fetch posts related to the logged-in user
    posts = BlogPost.objects.filter(user=request.user)
    
    # Initialize variables
    user_profile = None
    profile_image_url = None
    
    if request.user.is_authenticated:
        try:
            # Get the user profile if it exists
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            # Handle the case when the user profile does not exist
            user_profile = None
            profile_image_url = None
    
    # Pass variables to the template
    return render(request, 'studentPost/studentPost.html', {
        'posts': posts,
        'user_profile': user_profile,
        'profile_image_url': profile_image_url
    })

# def postDetail(request, post_id):
#     post = get_object_or_404(BlogPost, id=post_id)
#     related_posts = BlogPost.objects.filter(user=post.user).exclude(id=post.id)[:3]

#     user_profile = None
#     profile_image_url = None

#     if request.user.is_authenticated:
#         try:
#             user_profile = UserProfile.objects.get(user=post.user)
#             profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
#         except UserProfile.DoesNotExist:
#             user_profile = None
#             profile_image_url = None

#     # Fetch candidate preference related to the post
#     try:
#         candidate_preference = CandidatePreference.objects.get(blog_post=post)
#     except CandidatePreference.DoesNotExist:
#         candidate_preference = None      

#     return render(request, 'studentPost/postdetailes.html', {
#         'post': post,
#         'user_profile': user_profile,
#         'related_posts': related_posts,
#         'profile_image_url': profile_image_url,
#         'candidate_preference': candidate_preference  # Pass candidate preference to the template
#     })

def postDetail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    related_posts = BlogPost.objects.filter(user=post.user).exclude(id=post.id)[:3]

    post_author_profile = None
    post_author_image_url = None
    profile_image_url = None
    
    # Fetch the post author's profile image
    try:
        post_author_profile = UserProfile.objects.get(user=post.user)
        post_author_image_url = post_author_profile.profile_image.url if post_author_profile.profile_image else None
    except UserProfile.DoesNotExist:
        post_author_profile = None
        post_author_image_url = None


    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
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
        'post_author_image_url': post_author_image_url,
        'profile_image_url': profile_image_url,
        'related_posts': related_posts,
        'candidate_preference': candidate_preference  # Pass candidate preference to the template
    })


# View to show all posts with pagination
def all_posts(request):
    posts_list = BlogPost.objects.all().order_by('-publication_date')  # Fetch all posts
    paginator = Paginator(posts_list, 12)  # Show 12 posts per page
    page_number = request.GET.get('page', 1)  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)
    
    profile_image_url = None
    
    if request.user.is_authenticated:
        try:
            # Get the user profile if it exists
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            # Handle the case when the user profile does not exist
            user_profile = None
            profile_image_url = None

    context = {
        'posts': page_obj,
        'profile_image_url': profile_image_url,
    }
    return render(request, 'studentPost/all_posts.html', context)

# API view to load more posts dynamically
def load_more_posts(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 12)  # Show 12 posts per page
    page_number = request.GET.get('page', 1)  # Get the requested page number
    page_obj = paginator.get_page(page_number)

    posts_data = []
    for post in page_obj.object_list:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'image_url': post.blog_image.url if post.blog_image else None,
            'content': post.content[:100],  # Truncated content
            'user_first_name': post.user.first_name,
            'user_last_name': post.user.last_name,
            'user_profile_image': post.user.userprofile.profile_image.url if post.user.userprofile.profile_image else None,
        })

    return JsonResponse({
        'posts': posts_data,
        'has_next': page_obj.has_next(),  # To indicate if there are more posts
    })
    

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        # Bind the forms with POST data and uploaded files
        blog_post_form = BlogPostForm(request.POST)
        candidate_preference_form = CandidatePreferenceForm(request.POST)
        blog_image_form = BlogImageForm(request.POST, request.FILES)

        if blog_post_form.is_valid() and candidate_preference_form.is_valid() and blog_image_form.is_valid():
            # Save the blog post and attach the current user
            blog_post = blog_post_form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()

            # Save the candidate preference, associating it with the blog post
            candidate_preference = candidate_preference_form.save(commit=False)
            candidate_preference.blog_post = blog_post
            candidate_preference.save()

            # Save each image from the multiple image upload
            images = request.FILES.getlist('image')
            for image in images:
                BlogImage.objects.create(blog_post=blog_post, image=image)

            # Redirect to the desired page after successful post creation
            return redirect('studentpost')

    else:
        # Instantiate empty forms when GET request is made
        blog_post_form = BlogPostForm()
        candidate_preference_form = CandidatePreferenceForm()
        blog_image_form = BlogImageForm()

    # Fetch the profile image if the user has one, else set it to None
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None

    # Render the form page
    return render(request, 'studentPost/post_creation_form.html', {
        'blog_post_form': blog_post_form,
        'candidate_preference_form': candidate_preference_form,
        'blog_image_form': blog_image_form,
        'profile_image_url': profile_image_url,
    })

