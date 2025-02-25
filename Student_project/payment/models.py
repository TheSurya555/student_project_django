from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    is_indian_citizen = models.BooleanField()
    receive_invoices_via_email = models.BooleanField(default=False)
    
    # New fields for preferred candidate details
    preferred_candidate_name = models.CharField(max_length=255, blank=True, null=True)
    preferred_candidate_username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.full_name} Profile"

class Payment(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    candidate_username = models.CharField(max_length=255, default='default_username')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Razorpay-specific fields
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Payment from {self.recruiter.email} to {self.candidate_username} on {self.payment_date.strftime('%Y-%m-%d')}"


    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-payment_date']

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    custom_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Adding custom_amount
    description = models.TextField()
    short_content = models.TextField(blank=True, null=True)
    features = models.TextField()
    
    def __str__(self):
        return self.name