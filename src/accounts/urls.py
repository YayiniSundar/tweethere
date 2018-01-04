
from django.conf.urls import url,include
from django.views.generic.base import RedirectView

# from .views import tweet_detail_view, tweet_list_view, TweetDetailView, TweetListView
from .views import (
	UserDetailView,
	UserFollowView,
	)

urlpatterns = [
    # #url(r'^admin/', admin.site.urls),
    # url(r'^$', RedirectView.as_view(url="/")),
    # url(r'^search/$', TweetListView.as_view(), name='list'),
    # url(r'^create/$', TweetCreateView.as_view(), name='create'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'),
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'),
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'),
]