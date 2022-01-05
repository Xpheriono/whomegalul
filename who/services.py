import logging
import requests
import os

from django.core.cache import cache

logger = logging.getLogger('twitchLog')

class TwitchAPI:
    helix_url = 'https://api.twitch.tv/helix/'
    id_url = 'https://id.twitch.tv/oauth2/token'

    def __init__(self):
        logger.info('Twitch connection initiating')

    # Authorize the client with Twitch API if no existing access token
    def __authorize_client(self):
        data = {
            'client_id': os.environ['CLIENT_ID_WHO'],
            'client_secret': os.environ['SECRET_WHO'],
            'grant_type': 'client_credentials'
        }
        logger.info('Authorizing client...')
        try:
            rsp = requests.post(self.id_url, data=data)
            rsp.raise_for_status()
            if self.__cache_token(rsp.json()): # token was cached successfully
                logger.info('Client authorized and access token cached')
                return True
            else:
                logger.error('There was an error caching the access token')
        except requests.exceptions.Timeout as error:
            logger.error('Timed out while waiting for Twitch response')
        except requests.exceptions.RequestException as error:
            logger.error('Request:\n{} {} {}\n\nResponse:\n{} {}'.format(
                error.request.url, error.request.headers, error.request.body,
                error.response.headers, error.response.content
            ))

        return False

    # Cache the access token using Redis
    def __cache_token(self, rsp_json):
        token = {
            'token': rsp_json['access_token'],
            'expires_in': rsp_json['expires_in']
        }
        timeout = int(rsp_json['expires_in'])
        return cache.set('access_token', token, timeout=timeout)

    def __get_token(self):
        # Retrieve the access token from cache and verify client is authorized
        token = cache.get('access_token')
        if token is None:
            self.__authorize_client()
        return cache.get('access_token')

    # Retrieve a given twitch user by their username
    def get_user(self, username):
        token = self.__get_token()['token']

        # Build the HTTP request
        url = self.helix_url + 'users/'
        headers = {
            'Authorization': 'Bearer ' + token,
            'Client-Id': os.environ['CLIENT_ID_WHO']
        }
        params = {
            'login': username
        }

        return self.__make_request(url, headers, params)

    # Returns None on failure to make request
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