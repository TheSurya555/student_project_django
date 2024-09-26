from django.shortcuts import render, redirect
from.forms import ConsultingForm
from.models import *
from django.contrib import messages
from profiles.models import UserProfile

def consulting_View(request):
    if request.method == 'POST':
        form = ConsultingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will contact us soon')
            return redirect('contactus')
    else:
        form = ConsultingForm()

    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None
            
    support_info = SupportInfo.objects.all()         
    return render(request, 'contactus/consulting.html', {'form': form , 'profile_image_url':profile_image_url , 'support_info':support_info })
