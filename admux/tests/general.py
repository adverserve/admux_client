# coding: utf-8
import logging
log = logging.getLogger(__name__)

import httpretty

from django.test import TestCase

from adserver.client import Client

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


class LoginTest(LoginMixin, TestCase):

    def setUp(self):
        self.api = Client()

    @httpretty.activate
    def test_login(self):
        """Login to Api-Service"""

        api = self.api
        self.assertIsNone(api.api_key)

        key = self._login('strg', 'strg')

        self.assertEqual(self.api_key, key)
        self.assertEqual(self.api_key, api.api_key)
