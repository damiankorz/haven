from django.conf.urls import url 
from . import views 

urlpatterns = [
    url(r'^posts$', views.posts),
    url(r'^posts/process$', views.process_post),
    url(r'^posts/(?P<user_id>\d+)/(?P<post_id>\d+)/comment$', views.comment),
    url(r'^posts/(?P<user_id>\d+)/comment/(?P<comment_id>\d+)$', views.delete_comment),
]