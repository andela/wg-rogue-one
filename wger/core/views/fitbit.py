import os
import urllib
import base64
import requests


class Fitbit():
    '''
    Enables users get their weight and exercise information from fitbit
    '''

    SCOPE = ('weight', 'activity')

    def get_authorization_uri(self):
        # Get a unique URI for the user

        params = {
            'client_id': os.getenv('CLIENT_ID'),
            'response_type': 'code',
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'scope': ' '.join(self.SCOPE)
        }

        # encode the params
        encoded_params = urllib.parse.urlencode(params)
        return os.getenv('Authorization_URI') + '?' + encoded_params

    def get_access_token(self, code):
        # gets access_token if access_code passes the code_challenge

        # authentication header
        data_str = os.getenv('ACCESS_TOKEN') + ':' + os.getenv('CLIENT_SECRET')
        auth_header = base64.b64encode(data_str.encode('utf-8'))
        header = {
            'Authorization': os.getenv('Authorization'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': os.getenv('CLIENT_ID'),
            'redirect_uri': os.getenv('REDIRECT_URI'),
        }
        # request
        response = requests.post(os.getenv('ACCESS_TOKEN'), data=params, headers=header)
        resp = response.json()

        if response.status_code != 200:
            raise Exception("something went wrong (%s):%s" % (resp['errors'][0]['errorType'],
                                                              resp['errors'][0]['message']))

        # get our token
        token = dict()
        token['access_token'] = resp['access_token']
        token['refresh_token'] = resp['refresh_token']

        return token

    def refresh_access_token(self, token):
        # refreshes token after it has expired

        # authentication header
        auth_header = base64.b64encode(os.getenv('ACCESS_TOKEN') + ':' + os.getenv('CLIENT_SECRET'))
        header = {
            'Authorization': os.getenv('Authorization'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token['refresh_token']
        }

        # request
        response = requests.post(os.getenv('ACCESS_TOKEN'), data=params, headers=header)
        response = response.json()
        status_code = response.status_code

        if status_code != 200:
            raise Exception("something went wrong")

        # update our token
        token['access_token'] = response['access_token']
        token['refresh_token'] = response['refresh_token']

        return token

    def get_weight_info(self, token):
        # get user weight info from fitbit

        header = {
            'Authorization': 'Bearer %s' % token['access_token']
        }
        url = os.getenv('WEIGHT_URL')
        response = requests.get(url, headers=header)

        status_code = response.status_code
        if status_code == 200:
            return response.json()
        elif status_code == 401:
            # Invalid token, refresh token and fetch weight again
            token = self.refresh_access_token(token)
            self.get_weight_info(token)
        else:
            raise Exception("Action Failed")

    def get_exercise_info(self, token):
        # get user exercise info

        header = {
            'Authorization': 'Bearer %s' % token['access_token']
        }
        url = os.getenv('EXERCISE_URL')
        response = requests.get(url, headers=header)
        status_code = response.status_code

        if status_code == 200:
            return response.json()
        elif status_code == 401:
            # Invalid token, refresh token and fetch weight again
            token = self.refresh_access_token(token)
            self.get_exercise_info(token)
        else:
            raise Exception("Action Failed")
