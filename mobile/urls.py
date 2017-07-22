from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^ogp/$', OGP.as_view(), name='ogp'),
    url(r'^login/$', CustomizedLoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^paluwagan/(?P<pid>[0-9]+)/$', login_required(MyPaluwagan.as_view()), name='paluwagan'),
    url(r'^oauth/', include('social_django.urls'), name='social'),
    url(r'^howto/', login_required(HowTo.as_view()), name='howto'),
    url(r'^$', login_required(HomeView.as_view()), name='home'),
    url(r'^myaccount/$', login_required(MyPage.as_view()), name='mypage'),
    url(r'^ogp/$', OGP.as_view(), name='ogp'),
]
