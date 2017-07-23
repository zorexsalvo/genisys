# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

from social_django.models import UserSocialAuth
from django.contrib.auth.views import LoginView

from django.http import HttpResponseRedirect

import requests
import random
from . import config

class CustomizedLoginView(LoginView):
    def randomize_spiel(self):
        print('Generating spiel...')
        IMAGE_COLLECTION = [
            'http://easyhometutor.com/educationtimes/wp-content/uploads/2015/08/Role-of-Youth-in-Social-Welfare-Activities.jpg',
            'https://bcassets.starbucks.com/1612549662/1612549662_1140922324001_New-Orleans-589x331.jpg?pubId=1612549662',
            'https://www.philippinetintaawards.com/wp-content/uploads/2016/04/BIR-Bayanihan-A2.jpg',
            'https://c1.staticflickr.com/5/4141/4930852375_a85e4e5ae1_b.jpg',
        ]

        SPIEL_COLLECTION = [
            'See us before you GO!',
            'Help us build a loving world!',
        ]

        return [random.choice(IMAGE_COLLECTION), random.choice(SPIEL_COLLECTION)]

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.GET.get('next') is None:
            return HttpResponseRedirect('/')
        elif request.user.is_authenticated() and request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        return self.render_to_response(self.get_context_data())

class BaseView(TemplateView):
    def get_balance(self, fb_uid):
        try:
            url = config.SERVICE_HOST + '/pinoypaluwagan/index.php/autoexec/getUserBalance/{}'

            response = requests.get(url.format(fb_uid), timeout=10)
            balance = response.json()

            return balance.get('availableAmount')
        except Exception as e:
            return 0

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        url = 'https://graph.facebook.com/v2.10/{}/picture?redirect=0'
        user = request.user
        fb = UserSocialAuth.objects.get(user=request.user.id)

        response = requests.get(url.format(fb.uid), timeout=10)
        profile = response.json()
        context['profile_picture'] = profile['data']['url']
        context['balance'] = self.get_balance(fb.uid)

        return self.render_to_response(context)


class HomeView(BaseView):
    template_name = 'home.html'

    def get_paluwagan(self):
        try:
            url = config.SERVICE_HOST + '/pinoypaluwagan/index.php/autoexec/getCrowds'

            response = requests.get(url, timeout=10)
            paluwagans = response.json()
            return paluwagans['crowd']
        except Exception as e:
            return []

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['paluwagans'] = self.get_paluwagan()

        return context


class MyPage(BaseView):
    template_name = 'mypage.html'

    def get_balance(self, fb_uid):
        try:
            url = config.SERVICE_HOST + '/pinoypaluwagan/index.php/autoexec/getUserBalance/{}'

            response = requests.get(url.format(fb_uid), timeout=10)
            balance = response.json()

            return balance.get('availableAmount')
        except Exception as e:
            return 0

    def get_paluwagan(self, fb_uid):
        try:
            print('Getting the paluwagan..')
            url = config.SERVICE_HOST + '/pinoypaluwagan/index.php/autoexec/getUserCrowds/{}'
            response = requests.get(url.format(fb_uid), timeout=10)
            paluwagan = response.json()

            return response.json()['crowd']
        except Exception as e:
            print('Return empty array...')
            print(str(e))
            return []

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        url = 'https://graph.facebook.com/v2.10/{}/picture?redirect=0'
        user = request.user
        fb = UserSocialAuth.objects.get(user=request.user.id)

        response = requests.get(url.format(fb.uid), timeout=10)
        profile = response.json()
        context['profile_picture'] = profile['data']['url']
        context['balance'] = self.get_balance(fb.uid)
        context['paluwagan'] = self.get_paluwagan(fb.uid)

        return self.render_to_response(context)



class MyPaluwagan(BaseView):
    template_name = 'paluwagan.html'


class OGP(TemplateView):
    template_name = 'ogp.html'


class HowTo(BaseView):
    template_name = 'howto.html'
