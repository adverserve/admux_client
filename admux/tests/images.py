# coding: utf-8
import logging
log = logging.getLogger(__name__)

from StringIO import StringIO

import json
import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin
from adserver.tests.websites import WebsitesMixin
from adserver.tests.placements import PlacementsMixin
from adserver.tests.orders import OrdersMixin
from adserver.tests.campaigns import CampaignsMixin
from adserver.tests.creatives import CreativesMixin

class ImagesMixin(object):
    image_id = None

    @fake_requests
    def _images_list(self, *args, **kwargs):
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

        data = api.images(*args, **kwargs)
        self.image_id = data['images'][0]['uuid']

        return data

    @fake_requests
    def _image_delete(self, *args, **kwargs):
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

        data = api.image_delete(*args, **kwargs)
        return data

    @fake_requests
    def _image_create(self, *args, **kwargs):
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

        data = api.image_create(*args, **kwargs)
        self.image_id = data['image']

        return data


class AddImagesTest(ImagesMixin,
                    CreativesMixin, OrdersMixin, CampaignsMixin,
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

        self._creative_create(uuid=self.campaign_id,
                              html=self.creative_html,
                              placement=self.placement_id)


    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)
        self._creative_delete(uuid=self.creative_id)
        self._image_delete(uuid=self.image_id)


    @fake_requests
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
                       BaseMixin, TestCase):

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

    @fake_requests
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
                 BaseMixin, TestCase):

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


    @fake_requests
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


    @fake_requests
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


