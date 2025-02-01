from django.urls import path
from .views import *
from .views_aboutus import *
from .views_billing import *
from .views_profile import *
from .views_services import *
from .views_message import *
from .views_notification import *
from .views_progress import *
from .views_dashboard import *
from .views_homepage import *

urlpatterns = [
    path('', admin_login, name='admin_login'),
    
    path('dashboard/', dashboard, name='dashboard'),
    
    # profile urls
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    # Servie urls
    path('service/', service, name='service'),
    path('service/edit/<int:service_id>/', edit_service, name='edit_service'),
    path('service/add/', add_service, name='add_service'),
    path('service/<int:service_id>/delete/', delete_service, name='delete_service'),
    path('service_pages/add/', add_service_page, name='add_service_page'),
    path('service_pages/edit/<int:page_id>/', edit_service_page, name='edit_service_page'),
    path('service_pages/delete/<int:page_id>/', delete_service_page, name='delete_service_page'),
    
    # talent urls
    path('talentadmin/skill/add/', add_skill, name='add_skill'),
    path('talentadmin/skill/delete/<int:skill_id>/', delete_skill, name='delete_skill'),
    
    # examination urls
    path('examination/', examination, name='examination'),
    path('exam-add-skill/', exam_add_skill, name='exam_add_skill'),
    path('add-question/', add_question, name='add_question'),
    path('examination/edit_skill/<int:skill_id>/', exam_edit_skill, name='exam_edit_skill'),
    path('examination/delete_skill/<int:skill_id>/', exam_delete_skill, name='exam_delete_skill'),
    path('examination/edit_question/<int:question_id>/', edit_question, name='edit_question'),
    path('examination/delete_question/<int:question_id>/', delete_question, name='delete_question'),
    path('view-student-test/<int:user_id>/',view_student_test, name='view_student_test'),
    path('rules/add/', add_exam_rule, name='add_exam_rule'),
    path('rules/edit/<int:rule_id>/', edit_exam_rule, name='edit_exam_rule'),
    path('rules/delete/<int:rule_id>/', delete_exam_rule, name='delete_exam_rule'),
    path('update-test-score/<int:test_id>/', update_test_score, name='update_test_score'),
    path('test/delete/<int:test_id>/', delete_student_test, name='delete_student_test'),
    
    # about us urls
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
    path('support-info/add/', add_support_info, name='add_support_info'),
    path('support-info/edit/<int:info_id>/', edit_support_info, name='edit_support_info'),
    path('support-info/delete/<int:info_id>/', delete_support_info, name='delete_support_info'),    
    
    #Privacy Policy CURD URLs
    path('privacy-policy/add/', add_privacy_policy_content, name='add_privacy_policy_content'),
    path('privacy-policy/edit/<int:pk>/', edit_privacy_policy_content, name='edit_privacy_policy_content'),
    path('privacy-policy/delete/<int:pk>/', delete_privacy_policy_content, name='delete_privacy_policy_content'),
    
    # billing Urls
    path('billing/', billing, name='billing'),
    path('subscriptions/add/', add_subscription_view, name='add_subscription'),
    path('subscriptions/edit/<int:subscription_id>/', edit_subscription_view, name='edit_subscription'),
    path('subscriptions/delete/<int:subscription_id>/', delete_subscription_view, name='delete_subscription'),
    path('profile-pdf/<int:profile_id>/', profile_pdf, name='profile_pdf'),
    path('payment/<int:payment_id>/pdf/', payment_pdf, name='payment_pdf'),
    
    # Message urls
    path('admin-messages/', messages_view, name='admin_messages'),
    path('admin-messages/view/<int:message_id>/', view_message, name='view_message'),
    path('admin-messages/delete/<int:message_id>/', delete_consulting_message, name='delete_consulting_message'),
    
    # notification view
    path('notifications/', notification_view, name='notification_view'),
    path('notifications/mark-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    
    
    #project progress url
    
    path('projects/', project_list, name='project_list'),
    path('assign-project/', assign_project, name='assign_project'),
    path('edit-project/<int:project_id>/', edit_project, name='edit_project'),
    path('project/<int:project_id>/progress/', project_progress, name='admin_project_progress'),
    
    
    # Hero Section URLs
    path('admin/homepage/', admin_home_page, name='admin_home_page'),
    path('add_hero_section/', add_hero_section, name='add_hero_section'),
    path('edit_hero_section/<int:id>/', edit_hero_section, name='edit_hero_section'),
    path('delete_hero_section/<int:id>/', delete_hero_section, name='delete_hero_section'),
    
    # Work Step URLs
    path('add_work_step/', add_work_step, name='add_work_step'),
    path('edit_work_step/<int:id>/', edit_work_step, name='edit_work_step'),
    path('delete_work_step/<int:id>/', delete_work_step, name='delete_work_step'),
    
    # Contact Info URLs
    path('add_contact_info/', add_contact_info, name='add_contact_info'),
    path('edit_contact_info/<int:id>/', edit_contact_info, name='edit_contact_info'),
    path('delete_contact_info/<int:id>/', delete_contact_info, name='delete_contact_info'),
    
    # Footer URLs
    path('add_footer/', add_footer, name='add_footer'),
    path('edit_footer/<int:id>/', edit_footer, name='edit_footer'),
    path('delete_footer/<int:id>/', delete_footer, name='delete_footer'),

    # Portfolio Image URLs for Footer
    path('add_footer_portfolio_image/<int:footer_id>/', add_footer_portfolio_image, name='add_footer_portfolio_image'),
    path('edit_footer_portfolio_image/<int:footer_id>/<int:image_id>/', edit_footer_portfolio_image, name='edit_footer_portfolio_image'),
    path('delete_footer_portfolio_image/<int:footer_id>/<int:image_id>/', delete_footer_portfolio_image, name='delete_footer_portfolio_image'),
    path('manage_footer_portfolio_images/<int:footer_id>/', manage_footer_portfolio_images, name='manage_footer_portfolio_images'),

    # Admin logout url
    path('admin_logout/', admin_logout_view, name='admin_logout'),
    
]