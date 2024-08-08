from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:subscription_id>/', views.payment_page, name='payment_page'),
    # path('process_payment/<int:subscription_id>/', views.process_payment, name='process_payment'),
    path('edit_billing_info/<int:subscription_id>/', views.edit_billing_info, name='edit_billing_info'),
    path('payment-successful/', views.payment_successful, name='payment_successful'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),  # Added payment_callback URL
]
