from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .views import admin_required
from django.contrib.auth.decorators import login_required
from contactus.models import ConsultingMessage
from notifications.models import Notification

@login_required    
@admin_required
def messages_view(request):
    messages_list = ConsultingMessage.objects.all().order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]

    # Pagination logic
    paginator = Paginator(messages_list, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'messages_list': page_obj,  # Pass the paginated object
        'notifications': notifications,
    }
    return render(request, 'admin_customization/messages/messages.html', context)



@login_required
@admin_required
def view_message(request, message_id):
    message_obj = get_object_or_404(ConsultingMessage, id=message_id)

    context = {
        'message_obj': message_obj,
    }
    return render(request, 'admin_customization/messages/view_message.html', context)

@login_required
@admin_required
def delete_consulting_message(request, message_id):
    message = get_object_or_404(ConsultingMessage, id=message_id)
    message.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect('admin_messages')