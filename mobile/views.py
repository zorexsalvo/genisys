# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

import requests

class BaseView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        url = 'https://graph.facebook.com/v2.10/{}/picture?redirect=0'
        user = request.user
        fb = UserSocialAuth.objects.get(user=request.user.id)

        response = requests.get(url.format(fb.uid))
        profile = response.json()
        context['profile_picture'] = profile['data']['url']

        return self.render_to_response(context)


class LoginView(BaseView):
    template_name = 'login.html'


class HomeView(BaseView):
    template_name = 'home.html'

    
class MyPage(BaseView):
    template_name = 'mypage.html'


class MyPaluwagan(BaseView):
    template_name = 'paluwagan.html'


class OGP(TemplateView):
    template_name = 'ogp.html'
