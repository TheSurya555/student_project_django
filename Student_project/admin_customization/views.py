from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

def admin_login(request):
    if request.user.is_authenticated:
        # Redirect to the admin index if the user is already logged in
        return redirect(reverse('dashboard'))

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("Welcome, {}!").format(user.username))
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'site_header': _("TalentSprout Admin Login"),
    }
    return render(request, 'admin_customization/login.html', context)

    
def dashboard(request):
    return render(request, 'admin_customization/dashboard.html')