from django.contrib.auth.signals import user_logged_in
import requests
 
def update_user(sender, user, request, **kwargs):
    url = 'https://graph.facebook.com/v2.10/{}/picture?redirect=0'
    user = request.user
    fb = user.social_auth.get(provider='facebook').extra_data


    response = requests.get(url.format(fb.get('id')))
    profile = response.json()

    payload = {
        'facebookID': fb.get('id'),
        'firstName': user.first_name,
        'lastName': user.last_name,
        'emailAddr': user.email,
        'avatarURL': profile['data']['url']
    }
    
    print(payload)

   #  response = requests.post('http://192.168.167.208:8080/pinoypaluwagan/index.php/autoexec/registerUser',
                              # data=payload)

user_logged_in.connect(update_user)
