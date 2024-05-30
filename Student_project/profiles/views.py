from django.shortcuts import render

def profiles_View(request):
    return render(request, 'profiles/profiles.html')

def settings_View(request):
    # Retrieve user settings data from the database
    return render(request, 'profiles/settings.html')

def messages_View(request):
    # Retrieve user messages data from the database
    return render(request, 'profiles/messages.html')
