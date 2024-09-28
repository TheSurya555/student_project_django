from django.shortcuts import render, redirect
from .forms import ConsultingForm
from .models import *
from django.contrib import messages
from profiles.models import UserProfile
from notifications.signals import notify
from signUp.models import CustomUser 

def consulting_View(request):
    if request.method == 'POST':
        form = ConsultingForm(request.POST)
        if form.is_valid():
            # Save the form and send a success message
            consulting_message = form.save()
            messages.success(request, 'Your message has been sent successfully! We will contact you soon.')

            # Get admin users (filter based on your custom logic)
            admin_users = CustomUser.objects.filter(is_staff=True)

            # Send notification to all admin users
            for admin in admin_users:
                notify.send(
                    request.user, 
                    recipient=admin, 
                    verb='sent a new consulting message',
                    description=f'A new consulting message has been sent by {request.user.get_full_name()}.',
                    target=consulting_message
                )

            return redirect('contactus')
    else:
        form = ConsultingForm()

    # Get user profile image if the user is authenticated
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None

    # Get support information for the page
    support_info = SupportInfo.objects.all()

    return render(request, 'contactus/consulting.html', {
        'form': form, 
        'profile_image_url': profile_image_url, 
        'support_info': support_info 
    })
