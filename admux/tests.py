"""
Run "manage.py test"
"""
import logging
log = logging.getLogger(__name__)

import httpretty

from django.test import TestCase

from adserver.client import Client

class BaseTest(TestCase):
    test_api_key = "C96A2442-1322-11E3-9E33-96237FA36B44"

    def setUp(self):
        self.api = Client()

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : %s }' % self.test_api_key,
            content_type="application/json"
        )
        self.api.login('strg', 'strg')

        # initializing client without logging in
        self.fresh_api = Client()



class BasicTest(BaseTest):

    @httpretty.activate
    def test_login(self):
        api = self.fresh_api

        self.assertIsNone(api.api_key)

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "C96A2442-1322-11E3-9E33-96237FA36B44" }',
            content_type="application/json"
        )

        key = api.login('strg', 'strg')

        self.assertEqual("C96A2442-1322-11E3-9E33-96237FA36B44", key)
        self.assertEqual("C96A2442-1322-11E3-9E33-96237FA36B44", api.api_key)
