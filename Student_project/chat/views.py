from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import ChatSession, Message
from signUp.models import CustomUser
from django.db.models import Q
from django.contrib import messages as django_messages
from profiles.models import UserProfile
from notifications.models import Notification
from notifications.signals import notify

@login_required
def inbox(request):
    user = request.user
    received_messages = Message.objects.filter(receiver=user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=user).order_by('-timestamp')
    
    try:
        notifications = Notification.objects.filter(recipient=user)
        unread_notifications_count = notifications.unread().count()
        
    except Exception as e:
        notifications = [] 
        unread_notifications_count = 0 
        
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None      

    return render(request, 'chat/messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
        'profile_image_url':profile_image_url
    })
    
@login_required
@require_POST
def mark_notifications_as_read(request):
    try:
        request.user.notifications.mark_all_as_read()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def start_chat(request, candidate_id):
    candidate = get_object_or_404(CustomUser, id=candidate_id)
    recruiter = request.user

    # Ensure only one chat session between two users
    chat_session = ChatSession.objects.filter(
        participants=recruiter
    ).filter(participants=candidate).first()

    if not chat_session:
        chat_session = ChatSession.objects.create()
        chat_session.participants.add(recruiter, candidate)
    
    return redirect('chat_session', chat_session_id=chat_session.id)


@login_required
def chat_session(request, chat_session_id):
    user = request.user
    chat_session = get_object_or_404(ChatSession, id=chat_session_id)
    other_participant = chat_session.participants.exclude(id=user.id).first()
    received_messages = Message.objects.filter(receiver=user).order_by('-timestamp')
    
    # Debugging: check if the chat session exists
    print(f"Chat session: {chat_session.id}, User: {user.username}")
    # Fetch all messages for this chat session involving the current user
    messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('timestamp')


    # Fetch profile image of the logged-in user (if available)
    profile_image_url = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            profile_image_url = user_profile.profile_image.url if user_profile.profile_image else None
        except UserProfile.DoesNotExist:
            profile_image_url = None

    # Handle new message submission
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                chat_session=chat_session,
                sender=user,
                receiver=other_participant,
                content=content
            )
            notify.send(
                user,  # Sender of the notification
                recipient=other_participant,  # Receiver of the notification
                verb='sent you a message',
                description=f'New message: {content}',
                
            )
            return redirect('chat_session', chat_session_id=chat_session.id)

    # Render the chat session page with the required data
    return render(request, 'chat/chat_session.html', {
        'chat_session': chat_session,
        'messages': messages,
        'candidate': other_participant,
        'received_messages': received_messages,
        'user': user,
        'profile_image_url':profile_image_url,

    })


@login_required
def get_messages(request, chat_session_id):
    chat_session = get_object_or_404(ChatSession, id=chat_session_id)
    messages = chat_session.messages.all().order_by('timestamp')
    
    return JsonResponse({
        'messages': [{
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for message in messages]
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        to_username = request.POST.get('to_username')
        content = request.POST.get('message')
        recipient = get_object_or_404(CustomUser, username=to_username)

        if recipient:
            # Ensure only one chat session exists between sender and recipient
            chat_session = ChatSession.objects.filter(
                Q(participants=request.user) & Q(participants=recipient)
            ).first()
            
            if not chat_session:
                chat_session = ChatSession.objects.create()
                chat_session.participants.add(request.user, recipient)
            
            # Create and save the message
            Message.objects.create(
                chat_session=chat_session,
                sender=request.user,
                receiver=recipient,
                content=content,
            )

            # Notify the recipient about the new message
            notify.send(request.user, recipient=recipient, verb='sent you a message', description=content)

            django_messages.success(request, 'Message sent successfully!')
            return redirect('messages')
        else:
            django_messages.error(request, 'Recipient not found.')
            return redirect('compose')
