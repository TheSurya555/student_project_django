from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulting_View , name= 'consulting'),
    # path('consulting/success/', views.consulting_success, name='consulting_success'),
]