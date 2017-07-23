from django.contrib.auth.signals import user_logged_in
import requests

from . import config
 
def update_user(sender, user, request, **kwargs):
    try:
        print('Triggering signal...')
        url = 'https://graph.facebook.com/v2.10/{}/picture?redirect=0'
        user = request.user
        fb = user.social_auth.get(provider='facebook').extra_data


        response = requests.get(url.format(fb.get('id')), timeout=10)
        profile = response.json()

        payload = {
            'facebookID': fb.get('id'),
            'firstName': user.first_name,
            'lastName': user.last_name,
            'emailAddr': user.email,
            'avatarURL': profile['data']['url']
        }

        response = requests.post(config.SERVICE_HOST + '/pinoypaluwagan/index.php/autoexec/registerUser',
                                  data=payload,
                                  timeout=10)

        print(payload)
        if response.status_code not in [200, 201]:
            print(response.status_code)
            print('Error in updating user...')
            print(response.json())
        else:
            print('Login successfully')

    except Exception as e:
        print(str(e))
        print('Not an app user')

user_logged_in.connect(update_user)
