from django.shortcuts import render, redirect
from .forms import ConsultingForm
from .models import ConsultingMessage, SupportInfo
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

            # Prepare sender and target
            if request.user.is_authenticated:
                sender = request.user
                full_name = sender.get_full_name()
            else:
                sender = None  # No sender for anonymous users
                full_name = 'Anonymous'  # Use a placeholder for anonymous users

            # Send notification to all admin users
            for admin in admin_users:
                try:
                    # Ensure that consulting_message is valid
                    if consulting_message:
                        notify.send(
                            sender,  # This can be None for anonymous users
                            recipient=admin,
                            verb='sent a new consulting message',
                            description=f'A new consulting message has been sent by {full_name}.',
                            target=consulting_message  # Ensure this is a valid instance
                        )
                    else:
                        print("Consulting message is None.")
                except Exception as e:
                    print(f"Error sending notification: {e}")

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
