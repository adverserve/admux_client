# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import httpretty
import unittest

from .context import Client

from mixins.general import LoginMixin
from mixins.websites import WebsitesMixin
from mixins.placements import PlacementsMixin
from mixins.orders import OrdersMixin
from mixins.campaigns import CampaignsMixin
from mixins.clickwords import ClickwordsMixin
from mixins.creatives import CreativesMixin


class AddClickwordsTest(ClickwordsMixin,
                        CreativesMixin, OrdersMixin, CampaignsMixin,
                        PlacementsMixin, WebsitesMixin,
                        LoginMixin,
                        unittest.TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        self._get_websites()
        self._get_placements()

        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

        self._creative_create(uuid=self.campaign_id,
                              html=self.creative_html,
                              placement=self.placement_id)


    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)


    @httpretty.activate
    def test_create(self):
        ''' Creating clickword '''

        data = self._clickword_create(uuid=self.creative_id,
                                      tag=self.clickword_tag,
                                      url=self.clickword_url)
        self.assertTrue(u'clickword' in data)
        self.assertEquals(self.clickword_id, data[u'clickword'])

        self.assertTrue(u'job' in data)

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'tag' in request_body)
            self.assertTrue(u'url' in request_body)


class RemoveClickwordsTest(ClickwordsMixin,
                           CreativesMixin, OrdersMixin, CampaignsMixin,
                           PlacementsMixin, WebsitesMixin,
                           LoginMixin,
                           unittest.TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        self._get_websites()
        self._get_placements()

        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

        self._creative_create(uuid=self.campaign_id,
                              html=self.creative_html,
                              placement=self.placement_id)

        self._clickword_create(uuid=self.creative_id,
                               tag=self.clickword_tag,
                               url=self.clickword_url)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)

    @httpretty.activate
    def test_delete(self):
        ''' Deleting clickword '''
        data = self._clickword_delete(uuid=self.clickword_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)


class ClickwordsTest(ClickwordsMixin,
                     CreativesMixin, OrdersMixin, CampaignsMixin,
                     PlacementsMixin, WebsitesMixin,
                     LoginMixin,
                     unittest.TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        self._get_websites()
        self._get_placements()

        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

        self._creative_create(uuid=self.campaign_id,
                              html=self.creative_html,
                              placement=self.placement_id)

        self._clickword_create(uuid=self.creative_id,
                               tag=self.clickword_tag,
                               url=self.clickword_url)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)
        self._clickword_delete(uuid=self.clickword_id)


    @httpretty.activate
    def test_list(self):
        ''' List all clickwords '''

        data = self._clickwords_list(uuid=self.creative_id)
        self.assertTrue(u'clickwords' in data)

        data = self._clickwords_list(uuid=self.creative_id,
                                     links=True, expand=[ u'foo', ])
        self.assertTrue(u'clickwords' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'foo', ] })


    @httpretty.activate
    def test_detail(self):
        ''' List single clickword '''

        body = r'' \
            r'''
            {
                "created": "2013-10-15T13:12:12.000000",
                "tag": "tennisnet.com",
                "updated": "2013-10-15T13:12:12.000000",
                "url": "http://www.tennisnet.com",
                "uuid": "%s"
            }
            ''' % self.clickword_id
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



    @httpretty.activate
    def test_update(self):
        ''' Updating clickword '''

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
                                    tag=self.clickword_tag,
                                    url=self.clickword_url)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Updated', data[u'message'])

        self.assertTrue(u'job' in data)


