import logging
import requests
import os

from django.core.cache import cache
from requests.api import request # 'default' cache from settings

logger = logging.getLogger(__name__)

class TwitchAPI:
    helix_url = 'https://api.twitch.tv/helix/'
    id_url = 'https://id.twitch.tv/oauth2/token'

    def __init__(self):
        self.tokens = cache.get('access_token')
        # check if authorized, if not then authorize
        if self.tokens == None:
            if not self.__authorize_client():
                self.__handle_auth_error()

    def __authorize_client(self, force=False):
        data = {
            'client_id': os.environ['CLIENT_ID_WHO'],
            'client_secret': os.environ['SECRET_WHO'],
            'grant_type': 'client_credentials'
        }

        try:
            rsp = requests.post(self.id_url, data=data)
            rsp.raise_for_status()
            if self.cache_token(rsp.json()): # token was cached successfully
                logger.info('Token {} with {} seconds left was successfully cached'.format(
                    cache.get('access_token')['token'],
                    cache.get('access_token')['expires_in']
                ))
                return True
        except requests.exceptions.Timeout as error:
            logger.error('Timed out while waiting for Twitch response')
        except requests.exceptions.RequestException as error:
            logger.error('Request:\n{} {} {}\n\nResponse:\n{} {}'.format(
                error.request.url, error.request.headers, error.request.body,
                error.response.headers, error.response.content
            ))

        return False

    def __handle_auth_error(self):
        logger.error('auth error') # not sure how to handle yet, probably can't do much
        pass

    def cache_token(self, rsp_json, force=False):
        token = {
            'token': rsp_json['access_token'],
            'expires_in': rsp_json['expires_in']
        }
        if force:
            cache.set('access_token', token) # overwrites existing token
            return True
        return cache.add('access_token', token) # returns True if token does not exist already

    def get_user(self, username):
        token = self.tokens['token']
        if not token:
            self.__authorize_client()
            token = self.tokens['token']
        url = self.helix_url + 'users/'
        headers = {
            'Authorization': 'Bearer ' + token,
            'Client-Id': os.environ['CLIENT_ID_WHO']
        }
        params = {
            'login': username
        }

        return self.__make_request(url, headers, params)

    def __make_request(self, url, headers, payload):
        try:
            rsp = requests.get(url, headers=headers, params=payload)
            return rsp
        except requests.exceptions.RequestException as error:
            logger.error('Request:\n{} {} {}\n\nResponse:\n{} {}'.format(
                error.request.url, error.request.headers, error.request.body,
                error.response.headers, error.response.content
            ))
            return None

'''
helix/users response
{"data":[{"id":"772891","login":"xpheriono","display_name":"xpheriono","type":"","broadcaster_type":"","description":"","profile_image_url":"https://static-cdn.jtvnw.net/jtv_user_pictures/xpheriono-profile_image-f587b0ff400067b5-300x300.jpeg","offline_image_url":"","view_count":2311,"created_at":"2008-06-14T06:12:52.461775Z"}]}
'''