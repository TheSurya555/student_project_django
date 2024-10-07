from django.utils import timezone
from django.shortcuts import render
from signUp.models import CustomUser
from notifications.models import Notification
from .models import Traffic  # Import your Traffic model
from django.contrib.auth.decorators import login_required
from .views import admin_required
from django.db.models.functions import ExtractMonth, ExtractDay
from django.db.models import Count
from django.utils.timezone import now
import calendar
from payment.models import Payment
from datetime import timedelta


def log_traffic(request):
    # Check if traffic has already been logged for this session
    if not request.session.get('traffic_logged', False):
        Traffic.objects.create(
            user=request.user if request.user.is_authenticated else None,
            page_visited=request.path,  # Log the URL of the visited page
            ip_address=request.META.get('REMOTE_ADDR')  # Get the user's IP address
        )
        # Set the session variable to True to indicate traffic has been logged
        request.session['traffic_logged'] = True


@login_required    
@admin_required
def dashboard(request):
    # Log the traffic for both logged-in and non-logged-in users
    log_traffic(request)  # Call the logging function

    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
    
    # Retrieve all users first
    users = CustomUser.objects.all().order_by('-date_joined')

    # Separate users by roles
    candidates = users.filter(role=CustomUser.CANDIDATE)[:10]
    recruiters = users.filter(role=CustomUser.RECRUITER)[:10]
    
    # Aggregate registered users by month for the current year
    current_year = now().year
    users_by_month = CustomUser.objects.filter(date_joined__year=current_year) \
        .annotate(month=ExtractMonth('date_joined')) \
        .values('month') \
        .annotate(count=Count('id')) \
        .order_by('month')

    # Prepare data for the chart
    months = [calendar.month_name[i] for i in range(1, 13)]
    user_counts = [0] * 12  # Initialize with zeros for all months

    for entry in users_by_month:
        user_counts[entry['month'] - 1] = entry['count']
        
    # Aggregate traffic data by day for the current month
    current_month = now().month
    traffic_by_day = Traffic.objects.filter(timestamp__month=current_month) \
        .annotate(day=ExtractDay('timestamp')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')

    # Prepare data for the chart for traffic
    days = [i for i in range(1, 32)]  # Days of the month
    traffic_counts = [0] * 31  # Initialize with zeros for all days of the month

    for entry in traffic_by_day:
        traffic_counts[entry['day'] - 1] = entry['count']
    
    # fetch the payment information    
    payments = Payment.objects.all()  
    total_amount = sum(payment.amount for payment in payments)      
    
    # Calculate today's payments
    today = timezone.now().date()
    today_payments = Payment.objects.filter(payment_date__date=today)   # Assuming you have a 'date' field in Payment model
    today_amount = sum(payment.amount for payment in today_payments)


    # Calculate total users and today's new users
    total_users = CustomUser.objects.count()  # Total users
    today_users = CustomUser.objects.filter(date_joined__date=today).count() 
    
    # Total Recruiters
    total_recruiters = CustomUser.objects.filter(role=CustomUser.RECRUITER).count()
    # Calculate the start of the current quarter
    now_time = timezone.now()
    current_quarter = (now_time.month - 1) // 3 + 1
    quarter_start_month = (current_quarter - 1) * 3 + 1

    # Get the start of the last quarter
    last_quarter_start = (now_time.replace(month=quarter_start_month) - timedelta(days=90)).replace(day=1)
        # Recruiters who joined last quarter
    recruiters_last_quarter = CustomUser.objects.filter(
        role=CustomUser.RECRUITER, 
        date_joined__gte=last_quarter_start,
        date_joined__lt=now_time.replace(month=quarter_start_month, day=1)
    ).count()

    
    context = {
        'notifications': notifications,
        'months': months,
        'user_counts': user_counts,
        'candidates': candidates,
        'recruiters': recruiters,
        'days': days,
        'traffic_counts': traffic_counts,
        'total_amount': total_amount,
        'today_amount': today_amount,
        'total_users': total_users,
        'today_users': today_users,
        'total_recruiters': total_recruiters,
        'recruiters_last_quarter': recruiters_last_quarter, 
    }        
    
    return render(request, 'admin_customization/dashboard.html', context)
