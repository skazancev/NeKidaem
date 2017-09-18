from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^subscribe/$', views.SubscribeView.as_view(), name='subscribe'),
    url(r'^blog/create/$', views.PostCreateView.as_view(), name='create'),
    url(r'^blog/read/$', views.PostReadView.as_view(), name='read'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.BlogView.as_view(), name='user'),
    url(r'^blog/(?P<pk>[0-9]+)/delete/$', views.PostDeleteView.as_view(), name='delete'),
    url(r'^blog/(?P<user_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
]
