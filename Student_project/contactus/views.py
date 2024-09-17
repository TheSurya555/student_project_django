from django.shortcuts import render, redirect
from.forms import ConsultingForm
from.models import ConsultingMessage
from django.contrib import messages
from profiles.models import UserProfile

def consulting_View(request):
    if request.method == 'POST':
        form = ConsultingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will contact us soon')
            return redirect('consulting')
    else:
        form = ConsultingForm()
        
    user_profile = UserProfile.objects.get(user=request.user)
    profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
    return render(request, 'contactus/consulting.html', {'form': form , 'profile_image_url':profile_image_url })
