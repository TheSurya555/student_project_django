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

    def __str__(self):
        return f"{self.user.username} Profile"

class Payment(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment from {self.recruiter.email} to {self.candidate.email} on {self.payment_date}"
