from django.shortcuts import render

# Create your views here.
def services_View(request):
    return render(request,'services/services.html')