from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^home/(?P<user_id>\d+)$', views.home),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^addworkout$', views.addworkout),
    url(r'^going$', views.going),
    url(r'^follow$', views.follow),
    url(r'^cancel$', views.cancel),
    url(r'^edit$', views.edit),
    url(r'^update$', views.update),
    url(r'^logout$', views.logout),
    url(r'^showplace/(?P<going_id>\d+)$', views.showplace),
]