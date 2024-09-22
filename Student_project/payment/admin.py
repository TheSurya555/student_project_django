from django.contrib import admin
from .models import Profile, Payment, Subscription

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'full_name', 'company_name', 'country', 'state', 'city', 'postal_code', 
        'is_indian_citizen', 'receive_invoices_via_email', 'preferred_candidate_name', 'preferred_candidate_username'
    )
    search_fields = (
        'user__username', 'full_name', 'company_name', 'country', 'state', 'city', 
        'preferred_candidate_name', 'preferred_candidate_username'
    )
    list_filter = ('country', 'state', 'is_indian_citizen', 'receive_invoices_via_email')

admin.site.register(Profile, ProfileAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'candidate_username', 'amount', 'payment_date', 'status')
    search_fields = ('recruiter__email', 'candidate__user__username', 'amount', 'status')
    list_filter = ('payment_date', 'status')
    readonly_fields = ('razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature')

    def candidate_username(self, obj):
        return obj.candidate.user.username
    candidate_username.admin_order_field = 'candidate__user__username'  # Allows column sorting
    candidate_username.short_description = 'Candidate Username'
admin.site.register(Payment, PaymentAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description','short_content')
    search_fields = ('name', 'description')

admin.site.register(Subscription, SubscriptionAdmin)
