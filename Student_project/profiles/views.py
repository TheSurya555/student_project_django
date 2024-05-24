from django.shortcuts import render

# Create your views here.
def profiles_View(request):
    return render(request,'profiles/profiles.html')


def settings_View(request):
    return render(request,'profiles/settings.html')

def messages_View(request):
    return render(request,'profiles/messages.html')
