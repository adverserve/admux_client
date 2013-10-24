# coding: utf-8
import logging
log = logging.getLogger(__name__)

import httpretty
import unittest

from .context import Client

from mixins.general import LoginMixin

class LoginTest(LoginMixin, unittest.TestCase):

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
