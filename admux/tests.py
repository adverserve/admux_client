# coding: utf-8
"""
Run "manage.py test"
"""
import logging
log = logging.getLogger(__name__)

from datetime import datetime
import functools
import json
import httpretty
from StringIO import StringIO

from django.test import TestCase

from adserver.client import Client

FAKE_REQUESTS = True

def fake_requests(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if FAKE_REQUESTS:
            httpretty.reset()
            httpretty.enable()
            try:
                return func(*args, **kwargs)
            finally:
                httpretty.disable()
        else:
            return func(*args, **kwargs)
    return wrapper


class TestMixin(object):
    api_key = u"717A91DA-0BEE-11E3-9D78-B826E00120CD"

    website_id = u"67D02286-0968-11E3-B1D1-9E6D76D7A1E6"
    placement_id = u"953E93A6-0968-11E3-877B-F091A39B799E"

    order_id = u"F01CD8A0-3596-11E3-8D31-B4305DD555A5"
    order_name = u"test-order"
    adition_id = 24
    agency_id = 25
    client_id = 26

    campaign_id = u"F0F9FFF0-3596-11E3-ABFF-E3E78741F450"
    campaign_name = u"test-campaign"
    campaign_type = u"closedClicks"
    invalid_campaign_type = u"invalid"

    creative_id = u"67323CB0-359B-11E3-8723-959B3BBECF3D"

    clickword_id = u"67C93426-359B-11E3-8E16-80D11002FE68"

    image_id = u"C9819C44-1322-11E3-9E33-96237FA36B44"

    job_id = u"CA5434B0-1322-11E3-9E33-96237FA36B44"

    @fake_requests
    def _login(self):
        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "%s" }' % self.api_key,
            content_type="application/json"
        )
        return self.api.login(u'strg', u'strg')



class BasicTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()

    @fake_requests
    def test_login(self):
        """Login to Api-Service"""

        api = self.api

        self.assertIsNone(api.api_key)

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/login"),
            body='{ "api_key" : "717A91DA-0BEE-11E3-9D78-B826E00120CD" }',
            content_type="application/json"
        )

        key = api.login('strg', 'strg')

        self.assertEqual(self.api_key, key)
        self.assertEqual(self.api_key, api.api_key)


class WebsitesTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

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


class PlacementsTest(TestMixin, TestCase):
    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
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


        @fake_requests
        def test_detail(self):
            body = r'' \
                r'''
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


class OrdersTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
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


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
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


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
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


    @fake_requests
    def test_create(self):
        body = r'' \
            r'''
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

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'adition_id' in request_body)
            self.assertTrue(u'agency_id' in request_body)
            self.assertTrue(u'client_id' in request_body)


    @fake_requests
    def test_update(self):
        body = r'' \
            r'''
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



class CampaignsTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
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


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
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
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/campaigns/%s" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.campaign(uuid=self.campaign_id)
        self.assertTrue(u'uuid' in data)
        self.assertEquals(self.campaign_id, data[u'uuid'])


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
            {
                "message" : "Deleted",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/campaigns/%s" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.campaign_delete(uuid=self.campaign_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


    @fake_requests
    def test_create(self):
        body = r'' \
            r'''
            {
                "campaign" : "F0F9FFF0-3596-11E3-ABFF-E3E78741F450",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/orders/%s/campaigns" % self.order_id),
            body=body,
            content_type="application/json"
        )

        data = api.campaign_create(uuid=self.order_id, name=self.order_name)
        self.assertTrue(u'campaign' in data)
        self.assertEquals(self.campaign_id, data[u'campaign'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])

        data = api.campaign_create(uuid=self.order_id,
                                   name=self.campaign_name,

                                   adition_id=self.adition_id,
                                   campaign_type=self.campaign_type,
                                   total=500,
                                   priority=2,
                                   from_runtime=datetime.now(),
                                   to_runtime=datetime.now())

        self.assertTrue(u'campaign' in data)
        self.assertEquals(self.campaign_id, data[u'campaign'])

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'adition_id' in request_body)
            self.assertTrue(u'campaign_type' in request_body)
            self.assertTrue(u'total' in request_body)
            self.assertTrue(u'prioriry' in request_body)
            self.assertTrue(u'from_runtime' in request_body)
            self.assertTrue(u'to_runtime' in request_body)

        with self.assertRaises(ValueError):
            data = api.campaign_create(uuid=self.order_id,
                                       name=self.campaign_name,
                                       campaign_type=self.invalid_campaign_type)


    @fake_requests
    def test_update(self):
        body = r'' \
            r'''
            {
                "message" : "Updated",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.PUT,
            Client.get_url("/campaigns/%s" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.campaign_update(uuid=self.campaign_id,
                                   name=self.campaign_name)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


class CreativesTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
            {
                "creatives": [
                    {
                        "active": null,
                        "adition_id": "2173210",
                        "clickwords": [
                            "http://admux-demo.trust-box.at/v1/clickwords/67C93426-359B-11E3-8E16-80D11002FE68"
                        ],
                        "created": "2013-10-15T13:12:11.000000",
                        "html": "\n                                    <div class=\"darkensite\">Hello World</div>\n",
                        "images": [],
                        "name": "Advertorial_kurier_advertorial",
                        "placement": "http://admux-demo.trust-box.at/v1/placements/94DA4392-0968-11E3-8AE3-B86E7401D844",
                        "updated": "2013-10-16T16:03:11.000000",
                        "uuid": "67323CB0-359B-11E3-8723-959B3BBECF3D"
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/campaigns/%s/creatives" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.creatives(uuid=self.campaign_id)
        self.assertTrue(u'creatives' in data)

        data = api.creatives(uuid=self.campaign_id,
                             links=True, expand=[ u'clickwords', u'images', ])
        self.assertTrue(u'creatives' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'clickwords,images', ] })


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
            {
                "active": null,
                "adition_id": "2173210",
                "clickwords": [
                    "http://admux-demo.trust-box.at/v1/clickwords/67C93426-359B-11E3-8E16-80D11002FE68"
                ],
                "created": "2013-10-15T13:12:11.000000",
                "html": "\n                                    <div class=\"darkensite\">Hello World</div>\n",
                "images": [],
                "name": "Advertorial_kurier_advertorial",
                "placement": "http://admux-demo.trust-box.at/v1/placements/94DA4392-0968-11E3-8AE3-B86E7401D844",
                "updated": "2013-10-16T16:03:11.000000",
                "uuid": "67323CB0-359B-11E3-8723-959B3BBECF3D"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/creatives/%s" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.creative(uuid=self.creative_id)
        self.assertTrue(u'uuid' in data)
        self.assertEqual(self.creative_id, data[u'uuid'])

        data = api.creative(uuid=self.creative_id,
                            links=True, expand=[ u'clickwords', ])
        self.assertTrue(u'uuid' in data)


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
            {
                "message" : "Deleted",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/creatives/%s" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.creative_delete(uuid=self.creative_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


    @fake_requests
    def test_create(self):
        body = r'' \
            r'''
            {
                "creative" : "67323CB0-359B-11E3-8723-959B3BBECF3D",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/campaigns/%s/creatives" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.creative_create(uuid=self.campaign_id,
                                   html=u'<p>Foo</p>',
                                   placement=self.placement_id)
        self.assertTrue(u'creative' in data)
        self.assertEquals(self.creative_id, data[u'creative'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'html' in request_body)
            self.assertTrue(u'placement' in request_body)


    @fake_requests
    def test_update(self):
        body = r'' \
            r'''
            {
                "message" : "Updated",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.PUT,
            Client.get_url("/creatives/%s" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.creative_update(uuid=self.creative_id,
                                   html='<p>Foo</p>',
                                   placement=self.placement_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


class ClickwordsTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
            {
                "clickwords": [
                    {
                        "created": "2013-10-15T13:12:12.000000",
                        "tag": "wetter.at",
                        "updated": "2013-10-15T13:12:12.000000",
                        "url": "http://www.wetter.at",
                        "uuid": "6781F1CE-359B-11E3-B369-88EB2874B32D"
                    },
                    {
                        "created": "2013-10-15T13:12:12.000000",
                        "tag": "tennisnet.com",
                        "updated": "2013-10-15T13:12:12.000000",
                        "url": "http://www.tennisnet.com",
                        "uuid": "67C93426-359B-11E3-8E16-80D11002FE68"
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/creatives/%s/clickwords" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickwords(uuid=self.creative_id)
        self.assertTrue(u'clickwords' in data)

        data = api.clickwords(uuid=self.creative_id,
                              links=True, expand=[ u'foo', ])
        self.assertTrue(u'clickwords' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'foo', ] })


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
            {
                "created": "2013-10-15T13:12:12.000000",
                "tag": "tennisnet.com",
                "updated": "2013-10-15T13:12:12.000000",
                "url": "http://www.tennisnet.com",
                "uuid": "67C93426-359B-11E3-8E16-80D11002FE68"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/clickwords/%s" % self.clickword_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickword(uuid=self.clickword_id)
        self.assertTrue(u'uuid' in data)
        self.assertEqual(self.clickword_id, data[u'uuid'])

        data = api.clickword(uuid=self.clickword_id,
                             links=True, expand=[ u'clickwords', ])
        self.assertTrue(u'uuid' in data)


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
            {
                "message" : "Deleted",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/clickwords/%s" % self.clickword_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickword_delete(uuid=self.clickword_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


    @fake_requests
    def test_create(self):
        body = r'' \
            r'''
            {
                "clickword" : "67C93426-359B-11E3-8E16-80D11002FE68",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/creatives/%s/clickwords" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickword_create(uuid=self.creative_id,
                                    tag=u'foobar',
                                    url=u'http://foobar.com/some/path')
        self.assertTrue(u'clickword' in data)
        self.assertEquals(self.clickword_id, data[u'clickword'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'tag' in request_body)
            self.assertTrue(u'url' in request_body)


    @fake_requests
    def test_update(self):
        body = r'' \
            r'''
            {
                "message" : "Updated",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.PUT,
            Client.get_url("/clickwords/%s" % self.clickword_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickword_update(uuid=self.clickword_id,
                                    tag='foo',
                                    url='http://foobar.com/some/path')
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


class ImagesTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
            {
                "images": [
                    {
                       "created" : "2013-09-01T16:23:08.000000Z",
                       "filename" : "erdbeere.jpg",
                       "data" : "/9j/[..]KAUB//2Q==\n",
                       "updated" : "2013-09-01T16:23:08.000000Z",
                       "uuid" : "C9819C44-1322-11E3-9E33-96237FA36B44",
                       "links" : [
                          {
                             "rel" : "self",
                             "href" : "http://admux-demo.trust-box.at/v1/images/C9819C44-1322-11E3-9E33-96237FA36B44"
                          },
                          {
                             "rel" : "up",
                             "href" : "http://admux-demo.trust-box.at/v1/creatives/C97FA33A-1322-11E3-9E33-96237FA36B44"
                          }
                       ]
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/creatives/%s/images" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.images(uuid=self.creative_id)
        self.assertTrue(u'images' in data)

        data = api.images(uuid=self.creative_id,
                              links=True, expand=[ u'foo', ])
        self.assertTrue(u'images' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'foo', ] })


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
            {
               "created" : "2013-09-01T16:23:08.000000Z",
               "filename" : "erdbeere.jpg",
               "data" : "/9j/[..]KAUB//2Q==\n",
               "updated" : "2013-09-01T16:23:08.000000Z",
               "uuid" : "C9819C44-1322-11E3-9E33-96237FA36B44",
               "links" : [
                  {
                     "rel" : "self",
                     "href" : "http://admux-demo.trust-box.at/v1/images/C9819C44-1322-11E3-9E33-96237FA36B44"
                  },
                  {
                     "rel" : "up",
                     "href" : "http://admux-demo.trust-box.at/v1/creatives/C97FA33A-1322-11E3-9E33-96237FA36B44"
                  }
               ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/images/%s" % self.image_id),
            body=body,
            content_type="application/json"
        )

        data = api.image(uuid=self.image_id)
        self.assertTrue(u'uuid' in data)
        self.assertEqual(self.image_id, data[u'uuid'])

        data = api.image(uuid=self.image_id,
                             links=True, expand=[ u'foo', ])
        self.assertTrue(u'uuid' in data)


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
            {
                "message" : "Deleted",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/images/%s" % self.image_id),
            body=body,
            content_type="application/json"
        )

        data = api.image_delete(uuid=self.image_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


    @fake_requests
    def test_create(self):
        body = r'' \
            r'''
            {
                "image" : "C9819C44-1322-11E3-9E33-96237FA36B44",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/creatives/%s/images" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.image_create(uuid=self.creative_id,
                                file_name='sample.jpg',
                                file_object=StringIO("sample data"))
        self.assertTrue(u'image' in data)
        self.assertEquals(self.image_id, data[u'image'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'filename' in request_body)
            self.assertTrue(u'data' in request_body)


    @fake_requests
    def test_update(self):
        body = r'' \
            r'''
            {
                "message" : "Updated",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.PUT,
            Client.get_url("/images/%s" % self.image_id),
            body=body,
            content_type="application/json"
        )

        data = api.image_update(uuid=self.image_id,
                                file_name='sample.jpg',
                                file_object=StringIO("sample data"))
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


class JobsTest(TestMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login()

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
            {
                "jobs" : [
                    {
                        "status" : "todo",
                        "args" : {
                            "created" : "2013-09-01 16:23:09",
                            "name" : "New order",
                            "agency_id" : 43,
                            "user_id" : 2,
                            "updated" : "2013-09-01 16:23:09",
                            "id" : 9,
                            "uuid" : "CA538F42-1322-11E3-9E33-96237FA36B44"
                        },
                        "uuid" : "CA5434B0-1322-11E3-9E33-96237FA36B44",
                        "created" : "2013-09-01T16:23:09.000000Z",
                        "worker" : "InsertOrder",
                        "updated" : "2013-09-01T16:23:09.000000Z",
                        "links" : [
                                {
                                    "rel" : "self",
                                    "href" : "http://admux-demo.trust-box.at/v1/jobs/CA5434B0-1322-11E3-9E33-96237FA36B44"
                                }
                            ],
                        "result" : null
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/jobs"),
            body=body,
            content_type="application/json"
        )

        data = api.jobs()
        self.assertTrue(u'jobs' in data)

        data = api.jobs(links=True, expand=[ u'foo', ])
        self.assertTrue(u'jobs' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'foo', ] })


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
            {
                "status" : "todo",
                "args" : {
                    "created" : "2013-09-01 16:23:09",
                    "name" : "New order",
                    "agency_id" : 43,
                    "user_id" : 2,
                    "updated" : "2013-09-01 16:23:09",
                    "id" : 9,
                    "uuid" : "CA538F42-1322-11E3-9E33-96237FA36B44"
                },
                "uuid" : "CA5434B0-1322-11E3-9E33-96237FA36B44",
                "created" : "2013-09-01T16:23:09.000000Z",
                "worker" : "InsertOrder",
                "updated" : "2013-09-01T16:23:09.000000Z",
                "links" : [
                        {
                            "rel" : "self",
                            "href" : "http://admux-demo.trust-box.at/v1/jobs/CA5434B0-1322-11E3-9E33-96237FA36B44"
                        }
                    ],
                "result" : null
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/jobs/%s" % self.job_id),
            body=body,
            content_type="application/json"
        )

        data = api.job(uuid=self.job_id)
        self.assertTrue(u'uuid' in data)
        self.assertEqual(self.job_id, data[u'uuid'])

        data = api.job(uuid=self.job_id, links=True, expand=[ u'foo', ])
        self.assertTrue(u'uuid' in data)


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
            {
                "message" : "Deleted"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/jobs/%s" % self.job_id),
            body=body,
            content_type="application/json"
        )

        data = api.job_delete(uuid=self.job_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

