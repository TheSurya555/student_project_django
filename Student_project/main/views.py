from django.shortcuts import render

# Create your views here.
def layout_View(request):
    return render(request,'main/Layout.html')


def home_View(request):
    return render(request,'main/Index.html')