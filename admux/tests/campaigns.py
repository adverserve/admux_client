# coding: utf-8
import logging
log = logging.getLogger(__name__)

from datetime import datetime

import json
import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin


class CampaignsTest(BaseMixin, LoginMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

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
