from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:candidate_id>/', views.payment_page, name='payment_page'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('edit_billing_info/', views.edit_billing_info, name='edit_billing_info'),
     path('success/', views.success_page, name='success_page'),
]
