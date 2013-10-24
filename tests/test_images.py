# coding: utf-8
import logging
log = logging.getLogger(__name__)

from StringIO import StringIO

import json
import httpretty
import unittest

from .context import Client

from mixins.general import LoginMixin
from mixins.websites import WebsitesMixin
from mixins.placements import PlacementsMixin
from mixins.orders import OrdersMixin
from mixins.campaigns import CampaignsMixin
from mixins.creatives import CreativesMixin
from mixins.images import ImagesMixin


class AddImagesTest(ImagesMixin,
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
        self._image_delete(uuid=self.image_id)


    @httpretty.activate
    def test_create(self):
        ''' Creating image '''

        data = self._image_create(uuid=self.creative_id,
                                  file_name='sample.jpg',
                                  file_object=StringIO("sample data"))
        self.assertTrue(u'image' in data)
        self.assertEquals(self.image_id, data[u'image'])

        self.assertTrue(u'job' in data)

        if httpretty.httpretty.is_enabled():
            request_body = httpretty.last_request().body
            request_body = json.loads(request_body)

            self.assertTrue(u'filename' in request_body)
            self.assertTrue(u'data' in request_body)


class RemoveImagesTest(ImagesMixin,
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

        self._image_create(uuid=self.creative_id,
                           file_name='sample.jpg',
                           file_object=StringIO("sample data"))


    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)
        self._creative_delete(uuid=self.creative_id)

    @httpretty.activate
    def test_delete(self):
        ''' Deleting image '''
        data = self._image_delete(uuid=self.image_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)



class ImagesTest(ImagesMixin,
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

        self._images_list(uuid=self.creative_id)


    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)


    @httpretty.activate
    def test_list(self):
        ''' Listing images '''

        data = self._images_list(uuid=self.creative_id)
        self.assertTrue(u'images' in data)

        data = self._images_list(uuid=self.creative_id,
                                 links=True, expand=[ u'foo', ])
        self.assertTrue(u'images' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'foo', ] })


    @httpretty.activate
    def test_detail(self):
        ''' List details of single image '''

        body = r'' \
            r'''
            {
               "created" : "2013-09-01T16:23:08.000000Z",
               "filename" : "erdbeere.jpg",
               "data" : "/9j/[..]KAUB//2Q==\n",
               "updated" : "2013-09-01T16:23:08.000000Z",
               "uuid" : "%(image_id)s",
               "links" : [
                  {
                     "rel" : "self",
                     "href" : "http://admux-demo.trust-box.at/v1/images/%(image_id)s"
                  },
                  {
                     "rel" : "up",
                     "href" : "http://admux-demo.trust-box.at/v1/creatives/%(creative_id)s"
                  }
               ]
            }
            ''' % { 'image_id': self.image_id,
                    'creative_id': self.creative_id, }
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


    @httpretty.activate
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


