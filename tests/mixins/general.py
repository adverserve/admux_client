# coding: utf-8
import httpretty

from ..context import Client

class LoginMixin(object):
    credentials = ('strg', 'strg')

    @httpretty.activate
    def _login(self, *args, **kwargs):
        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "717A91DA-0BEE-11E3-9D78-B826E00120CD" }',
            content_type="application/json"
        )
        self.api_key = self.api.login(*args, **kwargs)

        return self.api_key
