from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatSession, Message
from signUp.models import CustomUser
from django.db.models import Q
from django.contrib import messages as django_messages
from profiles.models import UserProfile

@login_required
def inbox(request):
    user = request.user
    received_messages = Message.objects.filter(receiver=user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=user).order_by('-timestamp')

    return render(request, 'chat/messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

@login_required
def start_chat(request, candidate_id):
    candidate = get_object_or_404(CustomUser, id=candidate_id)
    recruiter = request.user

    # Ensure only one chat session between two users
    chat_session = ChatSession.objects.filter(participants=recruiter).filter(participants=candidate).first()

    if not chat_session:
        chat_session = ChatSession.objects.create()
        chat_session.participants.add(recruiter, candidate)
    
    return redirect('chat_session', chat_session_id=chat_session.id)

@login_required
def chat_session(request, chat_session_id):
    chat_session = get_object_or_404(ChatSession, id=chat_session_id)
    messages = chat_session.messages.all().order_by('timestamp')
    other_participant = chat_session.participants.exclude(id=request.user.id).first()

    # Print the received user's name and their message
    # Print statements for debugging
    print("Received user:", other_participant)
    for message in messages:
        print("Message content:", message.content)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                chat_session=chat_session, 
                sender=request.user, 
                receiver=other_participant,
                content=content
            )
            return redirect('chat_session', chat_session_id=chat_session.id)
    
    return render(request, 'chat/chat_session.html', {
        'chat_session': chat_session,
        'messages': messages,
        'candidate': other_participant,
        'user': request.user,
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
        to_email = request.POST.get('to')
        content = request.POST.get('message')
        recipient = get_object_or_404(CustomUser, email=to_email)

        if recipient:
            # Ensure only one chat session exists between sender and recipient
            chat_session = ChatSession.objects.filter(
                Q(participants=request.user) & Q(participants=recipient)
            ).first()
            
            if not chat_session:
                chat_session = ChatSession.objects.create()
                chat_session.participants.add(request.user, recipient)
            
            Message.objects.create(
                chat_session=chat_session,
                sender=request.user,
                receiver=recipient,
                content=content,
            )
            django_messages.success(request, 'Message sent successfully!')
            return redirect('messages')
        else:
            django_messages.error(request, 'Recipient not found.')
            return redirect('compose')
