# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin
from adserver.tests.campaigns import CampaignsMixin
from adserver.tests.orders import OrdersMixin
from adserver.tests.placements import PlacementsMixin
from adserver.tests.websites import WebsitesMixin

class CreativesMixin(object):
    creative_id = None

    creative_html = u'<p>Foo</p>'

    @fake_requests
    def _creatives_list(self, *args, **kwargs):
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
        self.creative_id = data['creatives'][0]['uuid']

        return data

    @fake_requests
    def _creative_delete(self, *args, **kwargs):
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

        return api.creative_delete(uuid=self.creative_id)


    @fake_requests
    def _creative_create(self, *args, **kwargs):
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

        data = api.creative_create(*args, **kwargs)
        self.creative_id = data['creative']

        return data


class AddCreativesTest(CreativesMixin, OrdersMixin, CampaignsMixin,
                       PlacementsMixin, WebsitesMixin,
                       LoginMixin,
                       BaseMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        self._get_websites()
        self._get_placements()

        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)


    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)

    @fake_requests
    def test_create(self):
        ''' Creating creative '''
        data = self._creative_create(uuid=self.campaign_id,
                                     html=self.creative_html,
                                     placement=self.placement_id)
        self.assertTrue(u'creative' in data)
        self.assertEquals(self.creative_id, data[u'creative'])

        self.assertTrue(u'job' in data)

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'html' in request_body)
            self.assertTrue(u'placement' in request_body)


class CreativesTest(CreativesMixin, OrdersMixin, CampaignsMixin,
                    PlacementsMixin, WebsitesMixin,
                    LoginMixin,
                    BaseMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        self._get_websites()
        self._get_placements()

        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

        self._creatives_create(uuid=self.campaign_id,
                               html=self.creative_html,
                               placement=self.placement_id)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)

    @fake_requests
    def test_delete(self):
        ''' Deleting creative '''
        data = self._creative_delete(uuid=self.creative_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)


class CreativesTest(CreativesMixin, OrdersMixin, CampaignsMixin,
                    PlacementsMixin, WebsitesMixin,
                    LoginMixin,
                    BaseMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        self._get_websites()
        self._get_placements()

        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

        self._creatives_list(uuid=self.campaign_id)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)

    @fake_requests
    def test_list(self):
        data = self._creatives_list(uuid=self.campaign_id)
        self.assertTrue(u'creatives' in data)

        data = self._creatives_list(uuid=self.campaign_id,
                                    links=True,
                                    expand=[ u'clickwords', u'images', ])
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
                "uuid": "%s"
            }
            ''' % self.creative_id
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
                                   html=self.creative_html,
                                   placement=self.placement_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)


