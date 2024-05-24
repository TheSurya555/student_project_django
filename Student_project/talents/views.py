from django.shortcuts import render

# Create your views here.
def talents_View (request):
    return render(request,'talents/talents.html')