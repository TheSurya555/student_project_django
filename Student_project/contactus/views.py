from django.shortcuts import render, redirect
from.forms import ConsultingForm
from.models import ConsultingMessage
from django.contrib import messages

def consulting_View(request):
    if request.method == 'POST':
        form = ConsultingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will contact us soon')
            return redirect('consulting')
    else:
        form = ConsultingForm()
    return render(request, 'contactus/consulting.html', {'form': form})
