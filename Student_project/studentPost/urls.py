from django.urls import path
from . import views

urlpatterns = [
    path('', views.studentPost , name= 'studentpost'),
    path('postdetail/<my_id>', views.postDetail , name= 'postdetail'),
    path('postform', views.postForm , name= 'postform'),
]