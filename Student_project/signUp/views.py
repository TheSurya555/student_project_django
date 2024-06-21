from django.shortcuts import render ,redirect
from django.contrib.auth import login ,logout ,authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from .forms import CandidateSignUpForm, RecruiterSignUpForm ,EmailOrPhoneLoginForm ,AdminSignUpForm
from .models import CustomUser


# Create your views here.
def signUP_View(request):
    return render(request,'signUp/chooseSignUp.html')


#candidate signup view
def candidate_SignUp_View(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            candidate_group = Group.objects.get(name='Candidate')
            user.groups.add(candidate_group)
            messages.success(request, 'Account Created Successfully !')
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
            user = form.save()
            # Assign the 'Recruiter' group to the user
            recruiter_group = Group.objects.get(name='Recruiter')
            user.groups.add(recruiter_group)
            messages.success(request, 'Account Created Successfully !')
            form = RecruiterSignUpForm()
        else:
            messages.error(request, 'Error while creating account !')
            print(messages.error)
    else:
        form = RecruiterSignUpForm()
    return render(request, 'signup/requiterSignup.html', {'form': form})

# Admin signup view
def admin_SignUp_View(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            admin_group = Group.objects.get(name='Admin')
            user.groups.add(admin_group)
            messages.success(request, 'Account Created Successfully !')
            form = AdminSignUpForm()
            print(form)
        else:
            messages.error(request, 'Error while creating account !')
    else:
        form = AdminSignUpForm()
    return render(request, 'signUp/adminSignup.html', {'form': form})
    

def login_View(request):
    return render(request,'signUp/chooselogin.html')

# candidate login view
def CandidateLoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request ,data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                print('user is' ,user )
                if user is not None:
                    login(request, user)
                    # Determine the user's role and store it in the session
                    if user.role == CustomUser.CANDIDATE:
                        request.session['user_role'] = 'Candidate'
                        print('Candidate logged in')
                        messages.success(request, 'Logged in successfully as Candidate!!')
                        return HttpResponseRedirect('/')  # Redirect to Candidate dashboard
                    else:
                        messages.error(request, 'Unknown user role!!')
                else:
                    messages.error(request, 'Bad credentials!!')
            else:
                messages.error(request, 'Bad credentials!!')
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signUp/candidateLogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/') # redirect to the home page
        
        
# Recruiter Login View     
        
def RecruiterLoginView(request):        
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request ,data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                print('user is' ,user )
                if user is not None:
                    login(request, user)
                    # Determine the user's role and store it in the session
                    if user.role == CustomUser.RECRUITER:
                        request.session['user_role'] = 'Recruiter'
                        print('Recruiter logged in')
                        messages.success(request, 'Logged in successfully as Recruiter!!')
                        return HttpResponseRedirect('/')  # Redirect to Recruiter dashboard
                    else:
                        messages.error(request, 'Unknown user role!!')
                else:
                    messages.error(request, 'Bad credentials!!')
            else:
                messages.error(request, 'Bad credentials!!')
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signUp/requiterLogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/') 
    
    
# Admin login view
def admin_LoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = EmailOrPhoneLoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                print('user is', user)
                if user is not None:
                    login(request, user)
                    # Determine the user's role and store it in the session
                    if user.role == CustomUser.ADMIN:
                        request.session['user_role'] = 'Admin'
                        print('Admin logged in')
                        messages.success(request, 'Logged in successfully as Admin!!')
                        return HttpResponseRedirect('/')  # Redirect to Admin dashboard
                    else:
                        messages.error(request, 'Unknown user role!!')
                else:
                    messages.error(request, 'Bad credentials!!')
            else:
                messages.error(request, 'Bad credentials!!')
        else:
            form = EmailOrPhoneLoginForm()
        return render(request, 'signUp/adminLogin.html', {'form': form})
    else:
        return HttpResponseRedirect('/')  # Redirect to the home page    
    
    
#logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

