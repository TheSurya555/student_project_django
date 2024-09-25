from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.studentPost , name= 'studentpost'),
    path('postdetail/<post_id>', views.postDetail , name= 'postdetail'),
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('all-posts/', views.all_posts, name='all_posts'),
    path('load-more-posts/', views.load_more_posts, name='load_more_posts'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


