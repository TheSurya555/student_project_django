from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:subscription_id>/', views.payment_page, name='payment_page'),
    path('process_payment/<int:subscription_id>/', views.process_payment, name='process_payment'),
    path('edit_billing_info/<int:subscription_id>/', views.edit_billing_info, name='edit_billing_info'),
    path('success/', views.success_page, name='success_page'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
]
