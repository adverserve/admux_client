"""
Run "manage.py test"
"""
import logging
log = logging.getLogger(__name__)

import json
import httpretty

from django.test import TestCase

from adserver.client import Client

class BaseTest(TestCase):
    api_key = u"C96A2442-1322-11E3-9E33-96237FA36B44"

    website_id = u"67D02286-0968-11E3-B1D1-9E6D76D7A1E6"
    placement_id = u"953E93A6-0968-11E3-877B-F091A39B799E"

    order_id = u"F01CD8A0-3596-11E3-8D31-B4305DD555A5"
    order_name = u"test-order"
    adition_id = 24
    agency_id = 25
    client_id = 26

    campaign_id = u"F0F9FFF0-3596-11E3-ABFF-E3E78741F450"

    job_id = u"CA5434B0-1322-11E3-9E33-96237FA36B44"

    def setUp(self):
        self.api = Client()

    @httpretty.activate
    def _login(self):
        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "%s" }' % self.api_key,
            content_type="application/json"
        )
        return self.api.login(u'strg', u'strg')



class BasicTest(BaseTest):

    @httpretty.activate
    def test_login(self):
        api = self.api

        self.assertIsNone(api.api_key)

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "C96A2442-1322-11E3-9E33-96237FA36B44" }',
            content_type="application/json"
        )

        key = api.login('strg', 'strg')

        self.assertEqual(u"C96A2442-1322-11E3-9E33-96237FA36B44", key)
        self.assertEqual(u"C96A2442-1322-11E3-9E33-96237FA36B44", api.api_key)


class WebsitesTest(BaseTest):

    def setUp(self):
        super(WebsitesTest, self).setUp()
        self._login()

    @httpretty.activate
    def test_list(self):
        body = '' \
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
            body=body,
            content_type="application/json"
        )

        data = api.websites()
        self.assertTrue(u'websites' in data)

        data = api.websites(links=True, expand=[ u'placements', ])
        self.assertTrue(u'websites' in data)

        self.assertEqual(httpretty.last_request().querystring,
                         { u'links': [ u'1', ],
                           u'expand': [ u'placements', ] })


    @httpretty.activate
    def test_detail(self):
        body = '' \
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


class PlacementsTest(BaseTest):
    def setUp(self):
        super(PlacementsTest, self).setUp()
        self._login()

    @httpretty.activate
    def test_list(self):
        body = '' \
            '''
            {
                "placements": [
                    {
                        "adition_id": "2566638",
                        "created": "2013-08-20T07:17:33.000000",
                        "height": 5,
                        "name": "kurier_sport_advertorial",
                        "type": "teaser",
                        "updated": "2013-08-20T07:17:33.000000",
                        "uuid": "953E93A6-0968-11E3-877B-F091A39B799E",
                        "width": 5
                    }
                ]
            }
        '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/websites/%s/placements" % self.website_id),
            body=body,
            content_type="application/json"
        )

        data = api.placements(uuid=self.website_id)
        self.assertTrue(u'placements' in data)


        @httpretty.activate
        def test_detail(self):
            body = '' \
                '''
                {
                    "adition_id": "2566638",
                    "created": "2013-08-20T07:17:33.000000",
                    "height": 5,
                    "name": "kurier_sport_advertorial",
                    "type": "teaser",
                    "updated": "2013-08-20T07:17:33.000000",
                    "uuid": "953E93A6-0968-11E3-877B-F091A39B799E",
                    "width": 5
                }
                '''
            api = self.api

            httpretty.register_uri(
                httpretty.GET,
                Client.get_url("/placements/%s" % self.placement_id),
                body=body,
                content_type="application/json"
            )

            data = api.placement(uuid=self.placement_id)
            self.assertTrue(u'uuid' in data)
            self.assertEquals(self.placement_id, data[u'uuid'])


class OrdersTest(BaseTest):

    def setUp(self):
        super(OrdersTest, self).setUp()
        self._login()

    @httpretty.activate
    def test_list(self):
        body = '' \
            '''
            {
                "orders": [
                    {
                        "adition_id": "109522",
                        "agency_id": "40125",
                        "campaigns": [
                            "http://admux-demo.trust-box.at/v1/campaigns/F0F9FFF0-3596-11E3-ABFF-E3E78741F450"
                        ],
                        "client_id": null,
                        "created": "2013-10-15T12:40:14.000000",
                        "name": "STRG",
                        "updated": "2013-10-16T06:57:52.000000",
                        "uuid": "F01CD8A0-3596-11E3-8D31-B4305DD555A5"
                    }
                ]
            }

            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/orders"),
            body=body,
            content_type="application/json"
        )

        data = api.orders()
        self.assertTrue(u'orders' in data)


    @httpretty.activate
    def test_detail(self):
        body = '' \
            '''
            {
                "adition_id": "2566638",
                "created": "2013-08-20T07:17:33.000000",
                "height": 5,
                "name": "kurier_sport_advertorial",
                "type": "teaser",
                "updated": "2013-08-20T07:17:33.000000",
                "uuid": "F01CD8A0-3596-11E3-8D31-B4305DD555A5",
                "width": 5
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/orders/%s" % self.order_id),
            body=body,
            content_type="application/json"
        )

        data = api.order(uuid=self.order_id)
        self.assertTrue(u'uuid' in data)
        self.assertEquals(self.order_id, data[u'uuid'])


    @httpretty.activate
    def test_delete(self):
        body = '' \
            '''
            {
                "message" : "Deleted",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/orders/%s" % self.order_id),
            body=body,
            content_type="application/json"
        )

        data = api.order_delete(uuid=self.order_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


    @httpretty.activate
    def test_create(self):
        body = '' \
            '''
            {
                "order" : "F01CD8A0-3596-11E3-8D31-B4305DD555A5",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/orders"),
            body=body,
            content_type="application/json"
        )

        data = api.order_create(name=self.order_name)
        self.assertTrue(u'order' in data)
        self.assertEquals(self.order_id, data[u'order'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])

        data = api.order_create(name=self.order_name,

                                adition_id=self.adition_id,
                                agency_id=self.agency_id,
                                client_id=self.client_id)
        self.assertTrue(u'order' in data)
        self.assertEquals(self.order_id, data[u'order'])

        request_body = httpretty.last_request().body
        request_body = json.loads(request_body)

        self.assertTrue(u'adition_id' in request_body)
        self.assertTrue(u'agency_id' in request_body)
        self.assertTrue(u'client_id' in request_body)


    @httpretty.activate
    def test_update(self):
        body = '' \
            '''
            {
                "message" : "Updated",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.PUT,
            Client.get_url("/orders/%s" % self.order_id),
            body=body,
            content_type="application/json"
        )

        data = api.order_update(uuid=self.order_id,
                                name=self.order_name)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])



class CampaignsTest(BaseTest):

    def setUp(self):
        super(CampaignsTest, self).setUp()
        self._login()

    @httpretty.activate
    def test_list(self):
        body = '' \
            '''
            {
                "campaigns": [
                    {
                        "active": null,
                        "adition_id": "536589",
                        "created": "2013-10-15T12:40:15.000000",
                        "creatives": [
                            "http://admux-demo.trust-box.at/v1/creatives/67323CB0-359B-11E3-8723-959B3BBECF3D"
                        ],
                        "from_runtime": "2013-10-15T12:40:18.000000",
                        "name": "",
                        "priority": 1,
                        "to_runtime": "2013-10-15T12:40:18.000000",
                        "total": null,
                        "type": "open",
                        "updated": "2013-10-16T16:03:11.000000",
                        "uuid": "F0F9FFF0-3596-11E3-ABFF-E3E78741F450"
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/orders/%s/campaigns" % self.order_id),
            body=body,
            content_type="application/json"
        )

        data = api.campaigns(self.order_id)
        self.assertTrue(u'campaigns' in data)


