from django.urls import path
from . import views
# from .views import  CandidateLoginView ,RecruiterLoginView

urlpatterns = [
    path('', views.signUP_View , name= 'signup'),
    path('candidateSignUp/', views.candidate_SignUp_View , name= 'candidateSignUp'),
    path('requiterSignUp/', views.requiter_SignUp_View, name= 'requiterSignUp'),
    path('candidatelogin/', views.CandidateLoginView , name='candidatelogin'),
    path('recruiterlogin/', views.RecruiterLoginView , name='recruiterlogin'),
    path('login/', views.login_View, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/roles/',  views.users_with_roles_view, name='users_with_roles'),
]