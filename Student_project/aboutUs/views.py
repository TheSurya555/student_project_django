from django.shortcuts import render

# Create your views here.
def aboutUs_view(request):
    return render(request, 'aboutUs/aboutUs.html') 