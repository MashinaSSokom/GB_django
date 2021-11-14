from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):

    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'domain')),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']
        if data['domain']:
            user.shopuserprofile.url = f'https://vk.com/{data["domain"]}'
        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age
        user.save()

    elif backend.name == 'github':
        if response['name']:
            name = response['name'].split(' ')
            user.first_name = name[0]
            user.last_name = name[1]

        if response['blog']:
            user.shopuserprofile.url = response['blog']

        if response['bio']:
            user.shopuserprofile.about_me = response['bio']

        user.save()

    else:
        return
