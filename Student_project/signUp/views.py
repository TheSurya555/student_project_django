from django.shortcuts import render

# Create your views here.
def signUP_View(request):
    return render(request,'signUp/chooseSignUp.html')


def candidate_SignUp_View(request):
    return render(request,'signUp/candidateSignup.html')