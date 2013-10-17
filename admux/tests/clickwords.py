# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin

class ClickwordsTest(BaseMixin, LoginMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

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


