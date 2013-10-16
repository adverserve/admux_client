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

