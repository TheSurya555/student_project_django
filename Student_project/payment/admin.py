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
    list_display = ('recruiter', 'get_preferred_candidate_username', 'amount', 'get_payment_method', 'payment_date')
    search_fields = ('recruiter', 'payment_method')
    list_filter = ('payment_method', 'payment_date')

    def get_preferred_candidate_username(self, obj):
        return obj.recruiter.profile.preferred_candidate_username if obj.recruiter.profile else None

    get_preferred_candidate_username.short_description = 'Preferred Candidate Username'
    
    def get_payment_method(self, obj):
        return obj.get_payment_method_display()  # Use get_payment_method_display() to show human-readable value
    
    get_payment_method.short_description = 'Payment Method'    

admin.site.register(Payment, PaymentAdmin) 

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')

admin.site.register(Subscription, SubscriptionAdmin)
