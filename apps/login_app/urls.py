from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    # url(r'^home$', views.home,
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^addworkout$', views.addworkout),
    url(r'^going$', views.going),
    url(r'^follow$', views.follow),
    # url(r'^logout$', views.logout),
]