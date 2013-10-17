# coding: utf-8
import logging
log = logging.getLogger(__name__)

import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin

class WebsitesTest(BaseMixin, LoginMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
            {
                "websites" : [
                   {
                      "name" : "Die Presse",
                      "uuid" : "C96A9030-1322-11E3-9E33-96237FA36B44",
                      "placements" : [
                         "http://admux-demo.trust-box.at/v1/placements/C96B4228-1322-11E3-9E33-96237FA36B44",
                         "http://admux-demo.trust-box.at/v1/placements/C96BE5DE-1322-11E3-9E33-96237FA36B44"
                      ],
                      "created" : "2013-09-01T16:23:08.000000Z",
                      "adition_id" : "816114",
                      "updated" : "2013-09-01T16:23:08.000000Z",
                      "advertorial_base_url" : "http://diepresse.at/advertorial/",
                      "links" : [
                         {
                            "rel" : "self",
                            "href" : "http://admux-demo.trust-box.at/v1/websites/C96A9030-1322-11E3-9E33-96237FA36B44"
                         }
                      ]
                   }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/websites"),
            body=body,
            content_type="application/json"
        )

        data = api.websites()
        self.assertTrue(u'websites' in data)

        data = api.websites(links=True, expand=[ u'placements', ])
        self.assertTrue(u'websites' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'placements', ] })


    @fake_requests
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
                "uuid": "67D02286-0968-11E3-B1D1-9E6D76D7A1E6"
            }
            '''
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
