from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('signup/', include('signUp.urls')),
    path('services/', include('services.urls')),
    path('talents/', include('talents.urls')),
    path('contactus/', include('contactus.urls')),
    path('profiles/', include('profiles.urls')),
    path('studentpost/', include('studentPost.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
