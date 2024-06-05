from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from .forms import BlogPostForm
from .models import BlogPost
from profiles.models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def studentPost(request):
    posts = BlogPost.objects.filter(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    return render(request, 'studentPost/studentPost.html', {'posts': posts ,'user_profile': user_profile ,'profile_image_url': profile_image_url })

@login_required

def postDetail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    related_posts = BlogPost.objects.filter(user=post.user).exclude(id=post.id)[:3]  # Fetch related posts by the same user, excluding the current post
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    return render(request, 'studentPost/postdetailes.html', {'post': post, 'user_profile': user_profile , 'related_posts': related_posts ,'profile_image_url': profile_image_url})


@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                blog_post = form.save(commit=False)
                blog_post.user = request.user  # Assign the current user
                blog_image = request.FILES.get('blog_image')
                if blog_image:
                    # Print debug information
                    print(f'Uploaded image name: {blog_image.name}')
                    print(f'Uploaded image size: {blog_image.size}')
                    max_filename_length = 1000
                    if len(blog_image.name) > max_filename_length:
                        blog_image.name = blog_image.name[:max_filename_length]
                    blog_post.blog_image = blog_image  # Save the image
                blog_post.save()
                messages.success(request, 'Blog post created successfully.')
                print('Blog post created successfully.')
                return redirect('studentpost')  # Redirect to a success page or the list of posts
            except ValidationError as e:
                error_messages = e.message_dict
                print(f'Validation errors: {error_messages}')
                form = BlogPostForm()
                return render(request, 'studentPost/post_creation_form.html', {'form': form, 'error_messages': error_messages})
            except Exception as e:
                messages.error(request, f'Error while creating the post: {e}')
                print(f'Error while creating the post: {e}')
        else:
            messages.error(request, 'Form is not valid. Please check the fields.')
            print('Form is not valid. Please check the fields.')
    else:
        form = BlogPostForm()
    return render(request, 'studentPost/post_creation_form.html', {'form': form})