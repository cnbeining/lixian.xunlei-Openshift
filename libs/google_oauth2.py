from tornado import httpclient
from tornado.auth import OAuth2Mixin
from tornado.concurrent import return_future
from tornado.httputil import url_concat
from tornado.escape import json_decode
from tornado.options import options
from httplib import HTTPSConnection
from urllib import urlencode
from functools import partial

class GoogleOAuth2Mixin(OAuth2Mixin):
    _OAUTH_HOST = "www.googleapis.com"
    _OAUTH_AUTHENTICATE_URL = "https://accounts.google.com/o/oauth2/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
    _OAUTH_TOKEN_VALIDATION_URL = "https://%s/oauth2/v1/tokeninfo" % _OAUTH_HOST
    _USER_INFO_PATH = "/oauth2/v1/userinfo"

    @property
    def httpclient_instance(self):
        return httpclient.AsyncHTTPClient()

    def authorize_redirect(self, scope, redirect_uri, **kwargs):
        args = {
            "redirect_uri": redirect_uri,
            "client_id": options.google_client_id,
            "response_type": "code",
            "scope": scope,
            "state": kwargs.get('state', '')
        }

        if kwargs:
            args.update(kwargs)

        url = url_concat(self._OAUTH_AUTHENTICATE_URL, args)

        self.redirect(url)

    @return_future
    def get_authenticated_user(self, authorization_code, redirect_uri, callback):
        args = {
            "client_id": options.google_client_id,
            "code": authorization_code,
            "client_secret": options.google_client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }

        body = urlencode(args)

        request = httpclient.HTTPRequest(self._OAUTH_ACCESS_TOKEN_URL, method="POST", body=body)

        self.httpclient_instance.fetch(request, partial(self._on_access_token, callback))

    def _on_access_token(self, callback, response):
        if not response or response.error:
            callback(None)
            return

        session = json_decode(response.body)

        self.validate_token(session, callback)

    def validate_token(self, session, callback):
        self.httpclient_instance.fetch(
            self._OAUTH_TOKEN_VALIDATION_URL + "?access_token=" + session['access_token'],
            partial(self.get_user_info, session, callback)
        )

    def get_user_info(self, session, callback, response):
        headers = {
            "Authorization": "Bearer " + session['access_token']
        }

        conn = HTTPSConnection(self._OAUTH_HOST)
        conn.request(
            "GET",
            self._USER_INFO_PATH + "?access_token=" + session['access_token'],
            "",
            headers
        )
        response = conn.getresponse()

        self._on_response(response, callback)

    def _on_response(self, response, callback):
        if not response or response.status != 200:
            callback(None)
            return

        user_info = json_decode(response.read())

        callback(user_info)
