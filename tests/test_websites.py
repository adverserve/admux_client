# coding: utf-8
import logging
log = logging.getLogger(__name__)

import httpretty
import unittest

from .context import Client

from mixins.general import LoginMixin
from mixins.websites import WebsitesMixin


class WebsitesTest(WebsitesMixin, LoginMixin,
                   unittest.TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._get_websites()

    @httpretty.activate
    def test_list(self):
        api = self.api

        data = self._get_websites()
        self.assertTrue(u'websites' in data)

        data = self._get_websites(links=True, expand=[ u'placements', ])
        self.assertTrue(u'websites' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'placements', ] })


    @httpretty.activate
    def test_detail(self):
        body = r'' \
            r'''
            {
                "adition_id": "38855",
                "advertorial_base_url": null,
                "created": "2013-08-20T07:16:17.000000",
                "name": "kurier",
                "placements": [
                    "http://admux-demo.trust-box.at/v1/placements/94DA4392-0968-11E3-8AE3-B86E7401D844",
                    "http://admux-demo.trust-box.at/v1/placements/953E93A6-0968-11E3-877B-F091A39B799E",
                    "http://admux-demo.trust-box.at/v1/placements/9577B046-0968-11E3-9A0D-B663F9BB9596",
                    "http://admux-demo.trust-box.at/v1/placements/976BB26C-0968-11E3-9AD2-C0060CC2BC6A"
                ],
                "updated": "2013-08-20T07:16:17.000000",
                "uuid": "%s"
            }
            ''' % self.website_id
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/websites/%s" % self.website_id),
            body=body,
            content_type="application/json"
        )

        data = api.website(uuid=self.website_id)
        self.assertTrue(u'uuid' in data)
        self.assertEqual(self.website_id, data[u'uuid'])

        data = api.website(uuid=self.website_id,
                           links=True, expand=[ u'placements', ])
        self.assertTrue(u'uuid' in data)
