from django.shortcuts import render

# Create your views here.
def studentPost(request):
    return render(request,'studentPost/studentPost.html')

def postDetail(request ,my_id):
    return render(request,'studentPost/postdetailes.html')

def postForm(request):
    return render(request,'studentPost/postform.html')
    