from django.contrib import admin
from django.urls import path ,include
from .views import *

urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('billing/', billing, name='billing'),
    path('service/', service, name='service'),
    path('service/edit/<int:service_id>/', edit_service, name='edit_service'),
    path('talentadmin/skill/add/', add_skill, name='add_skill'),
    path('talentadmin/skill/delete/<int:skill_id>/', delete_skill, name='delete_skill'),
    path('examination/', examination, name='examination'),
    path('exam-add-skill/', exam_add_skill, name='exam_add_skill'),
    path('add-question/', add_question, name='add_question'),
    path('examination/edit_skill/<int:skill_id>/', exam_edit_skill, name='exam_edit_skill'),
    path('examination/delete_skill/<int:skill_id>/', exam_delete_skill, name='exam_delete_skill'),
    path('examination/edit_question/<int:question_id>/', edit_question, name='edit_question'),
    path('examination/delete_question/<int:question_id>/', delete_question, name='delete_question'),
    path('view-student-test/<int:user_id>/',view_student_test, name='view_student_test'),
    path('admin_logout/', admin_logout_view, name='admin_logout'),
    
]