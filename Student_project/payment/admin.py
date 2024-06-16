from django.contrib import admin
from .models import Profile, Payment

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'company_name', 'country', 'state', 'city', 'postal_code', 'is_indian_citizen', 'receive_invoices_via_email')
    search_fields = ('user__username', 'full_name', 'company_name', 'country', 'state', 'city')
    list_filter = ('country', 'state', 'is_indian_citizen', 'receive_invoices_via_email')

admin.site.register(Profile, ProfileAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'candidate', 'amount', 'payment_method', 'payment_date')
    search_fields = ('recruiter__email', 'candidate__email', 'payment_method')
    list_filter = ('payment_method', 'payment_date')

admin.site.register(Payment, PaymentAdmin)
