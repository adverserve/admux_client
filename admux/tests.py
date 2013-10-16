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


class WebsitesTest(BaseTest):

    @httpretty.activate
    def test_list(self):
        list_body = '' \
            '''
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
            body=list_body,
            content_type="application/json"
        )

        data = api.websites()
        self.assertTrue('websites' in data)

        data = api.websites(links=True, expand=[ 'placements', ])
        self.assertTrue('websites' in data)

        self.assertEqual(httpretty.last_request().querystring,
                         { u'links': [ u'1', ],
                           u'expand': [ u'placements', ] })


    def test_detail(self):
        detail_body = '' \
            '''
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

        website_id = '67D02286-0968-11E3-B1D1-9E6D76D7A1E6'

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/website/%s" % website_id),
            body=detail_body,
            content_type="application/json"
        )

        data = api.website(uuid=website_id)
        self.assertTrue('uuid' in data)
        self.assertEqual(website_id, data['uuid'])

        data = api.website(uuid=website_id,
                           links=True, expand=[ 'placements', ])
        self.assertTrue('uuid' in data)
