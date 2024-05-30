from django.shortcuts import render ,redirect
from django.contrib.auth import login ,logout ,authenticate
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import CandidateSignUpForm, RecruiterSignUpForm ,EmailOrPhoneLoginForm
from django.urls import reverse_lazy

# Create your views here.
def signUP_View(request):
    return render(request,'signUp/chooseSignUp.html')


#candidate signup view
def candidate_SignUp_View(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Successfully !')
            form.save()
            form = CandidateSignUpForm()
        else:
            messages.error(request, 'Error while creating account !')
    else:
        form = CandidateSignUpForm()
    return render(request, 'signup/candidateSignup.html', {'form': form})

#requiter signup view
def requiter_SignUp_View(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Successfully !')
            form.save()
            form = RecruiterSignUpForm()
        else:
            messages.error(request, 'Error while creating account !')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'signup/requiterSignup.html', {'form': form})
    

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                print('user is :' ,user)
                if user is not None:
                    login(request, user)
                    # Determine the user's role and store it in the session
                    user_role = "Candidate" if user.groups.filter(name='Candidate').exists() else "Recruiter"
                    request.session['user_role'] = user_role
                    print(user_role)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/')  # Redirect to home or appropriate URL
                else:
                    messages.error(request, 'Bad credentials !!')
            else:
                messages.error(request, 'Bad credentials !!')
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signup/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')  # Redirect to home or appropriate URL if already authenticated
    

#logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
