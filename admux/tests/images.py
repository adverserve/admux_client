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

class ImagesTest(BaseMixin, LoginMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

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


