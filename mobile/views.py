# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth

import requests

class LoginView(TemplateView):
    template_name = 'login.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        url = 'https://graph.facebook.com/v2.10/{}/picture?redirect=0'

        fb = UserSocialAuth.objects.get(user=request.user.id)
        response = requests.get(url.format(fb.uid))
        profile = response.json()
        context['profile_picture'] = profile['data']['url']

        return self.render_to_response(context)


class MyPage(TemplateView):
    template_name = 'mypage.html'
