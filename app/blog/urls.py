from django.conf.urls import url
#from rest_framework import routers

from app.blog import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)

app_name = 'blog'

urlpatterns = [

    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^login/$', views.login),
    # url(r'^login/$', views.member, name='member'),
    #url(r'^logout/$', views.logout, name='logout'),

    url(r'^login/', views.login),
    url(r'^index/', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)/comment/', views.post_comment, name='post_comment'),
    url(r'^(?P<cmnt_id>[0-9]+)/del_cmnt/', views.del_comment, name='del_comment'),
    url(r'^login_user/', views.login_user, name='login_user'),

]

