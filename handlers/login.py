# -*- encoding: utf-8 -*-
# author: binux<17175297.hk@gmail.com>

from tornado.web import HTTPError, asynchronous
from tornado.options import options
from .base import BaseHandler
from libs.google_oauth2 import GoogleOAuth2Mixin


class LoginHandler(BaseHandler, GoogleOAuth2Mixin):
    @asynchronous
    def get(self):
        redirect_uri = "%s://%s/login" % (self.request.protocol, self.request.host)

        authorization_code = self.get_argument("code", None)
        if authorization_code:
            self.get_authenticated_user(authorization_code, redirect_uri, self._on_auth)
            return

        if self.get_argument("logout", None):
            self.clear_cookie("name", domain='.%s' % self.request.host, path='/')
            self.clear_cookie("email", domain='.%s' % self.request.host, path='/')
            self.redirect("/")
            return

        reg_key = self.get_argument("key", None)
        if reg_key:
            self.set_secure_cookie("reg_key", reg_key, expires_days=1, domain='.%s' % self.request.host, path='/')

        self.authorize_redirect(
            'profile email',
            redirect_uri
        )

    def _on_auth(self, user):
        if not user:
            self.set_status(500)
            self.finish("Google auth failed.")
            return

        if "zh" in user.get("locale", ""):
            chinese = False
            for word in user.get("name", ""):
                if ord(word) > 128:
                    chinese = True
                    break
            if chinese:
                user["name"] = user.get("family_name", "")+user.get("given_name", "")

        if options.reg_key:
            _user = self.user_manager.get_user(user["email"])
            reg_key = self.get_secure_cookie("reg_key", max_age_days=1)
            if not _user and reg_key != options.reg_key:
                self.set_status(403)
                self.finish("Registry is Disabled by Administrator.")
                return

        self.user_manager.update_user(user["email"], user["name"])
        self.set_secure_cookie("name", user["name"], expires_days=90, domain='.%s' % self.request.host, path='/')
        self.set_secure_cookie("email", user["email"], expires_days=90, domain='.%s' % self.request.host, path='/')
        self.redirect("/")

handlers = [
        (r"/login", LoginHandler),
]
ui_modules = {
}
