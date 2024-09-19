from django.urls import path
from .views import *
from .views_aboutus import *

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
    
    path('about-us/', admin_aboutus_view, name='admin_aboutus'),
    path('about-us/add/', add_aboutus_content, name='add_aboutus_content'),
    path('about-us/edit/<int:content_id>/', edit_aboutus_content, name='edit_aboutus_content'),
    path('about-us/delete/<int:content_id>/', delete_aboutus_content, name='delete_aboutus_content'),
    
    # Feature CRUD URLs
    path('about-us/feature/add/', add_feature, name='add_feature'),
    path('about-us/feature/edit/<int:feature_id>/', edit_feature, name='edit_feature'),
    path('about-us/feature/delete/<int:feature_id>/', delete_feature, name='delete_feature'),
    
    # Team Member CRUD URLs
    path('about-us/team/add/', add_team_member, name='add_team_member'),
    path('about-us/team/edit/<int:member_id>/', edit_team_member, name='edit_team_member'),
    path('about-us/team/delete/<int:member_id>/', delete_team_member, name='delete_team_member'),    
    
    # contact us CRUD URLs
    path('consulting-message/delete/<int:message_id>/', delete_consulting_message, name='delete_consulting_message'),
    path('support-info/add/', add_support_info, name='add_support_info'),
    path('support-info/edit/<int:info_id>/', edit_support_info, name='edit_support_info'),
    path('support-info/delete/<int:info_id>/', delete_support_info, name='delete_support_info'),    
    
    path('admin_logout/', admin_logout_view, name='admin_logout'),
    
]