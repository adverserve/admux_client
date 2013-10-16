"""
Run "manage.py test"
"""
import logging
log = logging.getLogger(__name__)

import httpretty

from django.test import TestCase

from adserver.client import Client

class ClientBasisTest(TestCase):

    def setUp(self):
        self.client = Client()

    @httpretty.activate
    def test_login(self):
        c = self.client

        self.assertIsNone(c.api_key)

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "C96A2442-1322-11E3-9E33-96237FA36B44" }',
            content_type="application/json"
        )

        key = c.login('strg', 'strg')

        self.assertEqual("C96A2442-1322-11E3-9E33-96237FA36B44", key)
        self.assertEqual("C96A2442-1322-11E3-9E33-96237FA36B44", c.api_key)
