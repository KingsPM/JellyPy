"""Objects for authenticating with the GEL CIP API."""

from __future__ import print_function, absolute_import
import json
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
import requests
from datetime import datetime, timedelta
from .auth_credentials import auth_credentials
from .config import live_100k_base_url, beta_testing_base_url, cva_base_url, opencga_base_url

#
# # get an authenticated session
# class AuthenticatedCIPAPISession(requests.Session):
#     """Subclass of requests Session for authenticating against GEL CIPAPI."""
#
#     def __init__(self, testing_on=False, token=None):
#         """Init AuthenticatedCIPAPISession and run authenticate function.
#
#         Authentication credentials are stored in auth_credentials.py and are in
#         dictionary format:
#
#         auth_credentials = {"username": "username", "password": "password"}
#
#         """
#         requests.Session.__init__(self)
#
#         if token:
#             self.update_token(token)
#         else:
#             self.authenticate(testing_on=testing_on)
#
#     def update_token(self, token):
#         """Update session token with a user supplied one.
#
#         Stores the JWT token and updates creation and expiration time from payload.
#
#         Returns:
#             The current instance of AuthenticatedCIPAPISession with the headers
#             set to include token, the auth_time and auth_expires time.
#         """
#
#         try:
#             decoded_token = jwt.decode(token, verify=False)
#             self.headers.update({"Authorization": "JWT " + token})
#             self.auth_time = datetime.fromtimestamp(decoded_token['orig_iat'])
#             self.auth_expires = datetime.fromtimestamp(decoded_token['exp'])
#         except (InvalidTokenError, DecodeError, ExpiredSignatureError, KeyError):
#             self.auth_time = False
#             raise Exception('Invalid or expired JWT token')
#         except:
#             raise
#
#         # Check whether the token has expired
#         if datetime.now() > self.auth_expires - timedelta(minutes=10):
#             raise Exception('JWT token has expired')
#         else:
#             pass
#
#         return self
#
#     def authenticate(self, testing_on=False):
#         """Use auth_credentials to generate an authenticated session.
#
#         Uses the cip_auth_url hard coded in and credentials in the
#         auth_credentials file to retrieve an authentication token from the CIP
#         API.
#
#         Returns:
#             The current instance of AuthenticatedCIPAPISession with the headers
#             set to include token, the auth_time and auth_expires time.
#         """
#
#         # Use the correct url if using beta dataset for testing:
#         if testing_on == False:
#             # Live data
#             cip_auth_url = (live_100k_base_url + 'get-token/')
#         else:
#             # Beta test data
#             cip_auth_url = (beta_testing_base_url + 'get-token/')
#
#         try:
#             token = (self.post(
#                 cip_auth_url, data=(auth_credentials))
#                 .json()['token'])
#             decoded_token = jwt.decode(token, verify=False)
#             self.headers.update({"Authorization": "JWT " + token})
#             self.auth_time = datetime.fromtimestamp(decoded_token['orig_iat'])
#             self.auth_expires = datetime.fromtimestamp(decoded_token['exp'])
#         except KeyError:
#             self.auth_time = False
#             raise Exception('Authentication Error')
#         except:
#             raise
#
#         return self


class AuthenticatedGelSession(requests.Session):
    """Subclass of requests Session for all GEL auth classes."""
    
    def __init__(self, token=None):
        # Call requests (parent) constructor
        super().__init__()

        # Initialised here, but defined in child class
        #self.auth_url = ""

        # Define required header parameters
        self.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

        # If a token is presented, confirm token validity, otherwise
        # use stored 'auth_credentials' details to authenticate
        if token:
            token_data = self.unpack_jwt_token(token)
        else:
            token, token_data = self.authenticate()

        # Add the token data as attributes. Items such as authenticated user can be used
        # to automatically 'stamp' actions such as closing cases
        for item in token_data.keys():
            self.item = token_data[item]

        # Add JWT token to auth header
        self.headers.update({
            "Authorization": "Bearer " + token
        })
        
    @staticmethod
    def unpack_jwt_token(token):
        """
        TODO
        :param token:
        :return:
        """
        try:
            decoded_token = jwt.decode(token, verify=False)
            token_data = {}
            for item in decoded_token.keys():
                if item in ('iat', 'exp', 'orig_iat'):
                    token_data[item] = datetime.fromtimestamp(decoded_token[item])
                else:
                    token_data[item] = decoded_token[item]

        except (InvalidTokenError, DecodeError, ExpiredSignatureError):
            raise Exception('Invalid Token')

        # Check whether the token has expired
        if datetime.now() > token_data['exp'] - timedelta(minutes=10):
            raise Exception('JWT token has expired')
        else:
            pass
        return token_data

    def authenticate(self):
        """
        TODO
        :return:
        """
        
        try:
            response = self.post(self.auth_url, data=json.dumps(auth_credentials), headers=self.headers).json()
            token = response['response'][0]['result'][0]['token']
        except KeyError:
            raise Exception('Authentication Error')
        except:
            raise
            
        token_data = self.unpack_jwt_token(token)

        return token, token_data


class AuthenticatedCIPAPISession(AuthenticatedGelSession):
    """
    TODO
    :return:
    """

    def __init__(self, api_version=2, testing_on=False, token=None):
        # Use the correct url if using beta dataset for testing:
        if testing_on:
            cip_base_url = beta_testing_base_url
        else:
            cip_base_url = live_100k_base_url

        self.auth_url = '{base_url}{api_version}/get-token/'.format(base_url=cip_base_url,
                                                                    api_version=api_version)

        print(self.auth_url)
        super().__init__(token=token)

    def authenticate(self):
        """
        TODO
        :return:
        """

        try:
            response = self.post(self.auth_url, data=json.dumps(auth_credentials), headers=self.headers).json()
            token = response['token']
        except KeyError:
            raise Exception('Authentication Error')
        except:
            raise

        token_data = self.unpack_jwt_token(token)

        return token, token_data


class AuthenticatedOpenCGASession(AuthenticatedGelSession):
    """
    TODO
    :return:
    """
    
    def __init__(self, api_version='v1', token=None):
        
        self.auth_url = '{base_url}{api_version}/users/{username}/login'.format(
                                        base_url=opencga_base_url,
                                        api_version=api_version,
                                        username=auth_credentials['username'])
        
        super().__init__(token=token)


class AuthenticatedCVASession(AuthenticatedGelSession):
    """
    TODO
    :return:
    """
    
    def __init__(self, api_version=0, token=None):
        
        self.auth_url = '{base_url}{api_version}/authentication'.format(
                                                        base_url=cva_base_url, 
                                                        api_version=api_version)

        super().__init__(token=token)
