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
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('upi', 'UPI'),
        # Add more choices as needed
    ]
    
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    candidate = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)

    def candidate_username(self):
        return self.candidate.user.username

    def __str__(self):
        return f"Payment from {self.recruiter.email} to {self.candidate_username()} on {self.payment_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-payment_date']

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    features = models.TextField()

    def __str__(self):
        return self.name
