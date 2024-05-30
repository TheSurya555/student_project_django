from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserProfileForm

# Create your views here.
def profiles_View(request):
    if request.user.is_authenticated:
        user = request.user
    return render(request,'profiles/profiles.html' ,{'user' : user})


def settings_View(request):
    return render(request,'profiles/settings.html')

def messages_View(request):
    return render(request,'profiles/messages.html')


def edit_profile_View(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profiles')  # Redirect to the profile view after successful update
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})