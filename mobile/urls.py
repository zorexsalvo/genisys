from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls'), name='social'),
    url(r'^$', login_required(HomeView.as_view()), name='home'),
    url(r'^myaccount/$', login_required(MyPage.as_view()), name='mypage'),
]
