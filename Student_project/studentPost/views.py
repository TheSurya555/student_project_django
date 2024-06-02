from django.shortcuts import render ,redirect

# Create your views here.
def studentPost(request):
    return render(request,'studentPost/studentPost.html')

def postDetail(request ,my_id):
    return render(request,'studentPost/postdetailes.html')


from django.shortcuts import render, redirect
from .forms import BlogPostForm

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_success')  # Redirect to a success page
    else:
        form = BlogPostForm()
    return render(request, 'studentPost/post_creation_form.html', {'form': form})

    