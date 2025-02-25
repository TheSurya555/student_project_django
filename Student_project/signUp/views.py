from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .forms import CandidateSignUpForm, RecruiterSignUpForm, EmailOrPhoneLoginForm, AdminSignUpForm
from .tokens import email_verification_token
from .models import CustomUser

User = get_user_model()

def signUP_View(request):
    return render(request, 'signUp/chooseSignUp.html')

def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your Talent Sprout account.'
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user),
    }
    message = render_to_string('signup/email_verification.html', context)
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"  # Ensures the email is sent as HTML
    email.send()
    
def candidate_SignUp_View(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                candidate_group = Group.objects.get(name='Candidate')
                user.groups.add(candidate_group)
                send_verification_email(request, user)
                messages.success(request, 'Account created successfully! Please check your email to verify your account.')
                return redirect('email_verification_notification')
            except Group.DoesNotExist:
                messages.error(request, 'Candidate group does not exist. Please contact support.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Error while creating account!')
    else:
        form = CandidateSignUpForm()
    return render(request, 'signup/candidateSignup.html', {'form': form})

def requiter_SignUp_View(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                recruiter_group = Group.objects.get(name='Recruiter')
                user.groups.add(recruiter_group)
                send_verification_email(request, user)
                messages.success(request, 'Account created successfully! Please check your email to verify your account.')
                return redirect('email_verification_notification')
            except Group.DoesNotExist:
                messages.error(request, 'Recruiter group does not exist. Please contact support.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Error while creating account!')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'signup/requiterSignup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, 'Your email has been verified successfully. Please log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('login')

def admin_SignUp_View(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                admin_group = Group.objects.get(name='Admin')
                user.groups.add(admin_group)
                send_verification_email(request, user)
                messages.success(request, 'Account created successfully! Please check your email to verify your account.')
                return redirect('email_verification_notification')
            except Group.DoesNotExist:
                messages.error(request, 'Admin group does not exist. Please contact support.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Error while creating account!')
    else:
        form = AdminSignUpForm()
    return render(request, 'signUp/adminSignup.html', {'form': form})

def email_verification_notification(request):
    return render(request, 'signUp/email_verification_notification.html')


def login_View(request):
    return render(request, 'signUp/chooselogin.html')

def CandidateLoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    if user.email_verified:
                        login(request, user)
                        if user.role == CustomUser.CANDIDATE:
                            request.session['user_role'] = 'Candidate'
                            messages.success(request, 'Logged in successfully as Candidate!!')
                            return HttpResponseRedirect('/')
                        else:
                            messages.error(request, 'Unknown user role!!')
                    else:
                        messages.error(request, 'Email is not verified. Please verify your email to log in.')
                else:
                    messages.error(request, 'Invalid username or password!')
            else:
                for field in form.errors:
                    messages.error(request, f" {form.errors[field][0]}")
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signUp/candidateLogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/')

def RecruiterLoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    if user.email_verified:
                        login(request, user)
                        if user.role == CustomUser.RECRUITER:
                            request.session['user_role'] = 'Recruiter'
                            messages.success(request, 'Logged in successfully as Recruiter!!')
                            return HttpResponseRedirect('/')
                        else:
                            messages.error(request, 'Unknown user role!!')
                    else:
                        messages.error(request, 'Email is not verified. Please verify your email to log in.')
                else:
                    messages.error(request, 'Invalid username or password!')
            else:
                for field in form.errors:
                    messages.error(request, f"{form.errors[field][0]}")
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signUp/requiterLogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def admin_LoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    if user.email_verified:
                        login(request, user)
                        if user.role == CustomUser.ADMIN:
                            request.session['user_role'] = 'Admin'
                            messages.success(request, 'Logged in successfully as Admin!!')
                            return HttpResponseRedirect('/')
                        else:
                            messages.error(request, 'Unknown user role!!')
                    else:
                        messages.error(request, 'Email is not verified. Please verify your email to log in.')
                else:
                    messages.error(request, 'Invalid username or password!')
            else:
                for field in form.errors:
                    messages.error(request, f" {form.errors[field][0]}")
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signUp/adminLogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    return redirect('login')
