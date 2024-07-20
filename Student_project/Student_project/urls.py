from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from main import views as main_views

urlpatterns = [
    path('sproutadmin/', admin.site.urls),
    path('', include('main.urls')),
    path('signup/', include('signUp.urls')),
    path('services/', include('services.urls')),
    path('talents/', include('talents.urls')),
    path('contactus/', include('contactus.urls')),
    path('profiles/', include('profiles.urls')),
    path('studentpost/', include('studentPost.urls')),
    path('chat/', include('chat.urls')),
    path('payment/', include('payment.urls')),
    path('examination/', include('examination.urls')),
    path('aboutUs-talent/', include('aboutUs.urls')),
    path('', include('password_reset.urls')),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handler for 404 errors
handler404 = 'main.views.custom_404'