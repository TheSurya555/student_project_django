from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:subscription_id>/', views.payment_page, name='payment_page'),
    path('edit_billing_info/<str:subscription_id>/', views.edit_billing_info, name='edit_billing_info'),
    path('payment-successful/', views.payment_successful, name='payment_successful'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),  # Added payment_callback URL
    path('custom-payment/', views.custom_payment, name='custom_payment'),# Added custom_paymentwesdcfv URL
]
