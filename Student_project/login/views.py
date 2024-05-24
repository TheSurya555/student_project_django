from django.shortcuts import render

# Create your views here.
def login_View(request):
    return render(request,'login/login.html')