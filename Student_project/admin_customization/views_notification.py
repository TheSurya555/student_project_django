from django.http import JsonResponse
from django.shortcuts import render
from notifications.models import Notification
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
@require_POST
def mark_notifications_as_read(request):
    notifications = Notification.objects.filter(recipient=request.user, unread=True)
    notifications.update(unread=False)
    
    return JsonResponse({'success': True})


def notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    all_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    unread_count = Notification.objects.filter(recipient=request.user, unread=True).count()
    
    paginator = Paginator(all_notifications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context ={
        'all_notifications': page_obj,
        'notifications': notifications ,
        'unread_count': unread_count,
    }

    return render(request, 'admin_customization/notification/notifications.html',context)