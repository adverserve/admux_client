# coding: utf-8
import logging
log = logging.getLogger(__name__)

from datetime import datetime
from uuid import uuid4

import json
import httpretty

from django.test import TestCase

from adserver.admux.client import Client
from adserver.tests.general import LoginMixin
from adserver.tests.orders import OrdersMixin


class CampaignsMixin(object):
    campaign_id = None

    campaign_name = u"test-campaign-%s" % uuid4()
    campaign_type = u"closedClicks"
    invalid_campaign_type = u"invalid"

    @httpretty.activate
    def _campaigns_list(self, *args, **kwargs):
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

        data = api.campaigns(*args, **kwargs)
        self.campaign_id = data['campaigns'][0]['uuid']

        return data

    @httpretty.activate
    def _campaign_delete(self, *args, **kwargs):
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
        self.campaign_id = None

        return data

    @httpretty.activate
    def _campaign_create(self, *args, **kwargs):
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

        data = api.campaign_create(*args, **kwargs)
        self.campaign_id = data['campaign']

        return data


class AddCampaignsTest(CampaignsMixin, OrdersMixin, LoginMixin,
                       TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._order_create(name=self.order_name)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)

    @httpretty.activate
    def test_create(self):
        """ Creating a simple campaign """
        data = self._campaign_create(uuid=self.order_id, name=self.campaign_name)
        self.assertTrue(u'campaign' in data)
        self.assertEquals(self.campaign_id, data[u'campaign'])

        self.assertTrue(u'job' in data)

    @httpretty.activate
    def test_create_complex(self):
        """ Creating a complex campaign """

        data = self._campaign_create(uuid=self.order_id,
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

    @httpretty.activate
    def test_create_invalid(self):
        """ reate campaign for invalid campaign-type """

        with self.assertRaises(ValueError):
            data = self._campaign_create(
                uuid=self.order_id,
                name=self.campaign_name,
                campaign_type=self.invalid_campaign_type
            )


class RemoveCampaignsTest(CampaignsMixin, OrdersMixin, LoginMixin,
                          TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)

    @httpretty.activate
    def test_delete(self):
        """ Removing campaign """
        data = self._campaign_delete(uuid=self.campaign_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)


class CampaignsTest(CampaignsMixin, OrdersMixin, LoginMixin,
                    TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._order_create(name=self.order_name)
        self._campaign_create(uuid=self.order_id, name=self.campaign_name)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)
        self._campaign_delete(uuid=self.campaign_id)

    @httpretty.activate
    def test_list(self):
        """ Listing campaigns """
        data = self._campaigns_list(uuid=self.order_id)
        self.assertTrue(u'campaigns' in data)


    @httpretty.activate
    def test_detail(self):
        """ Listing one campaign """
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
                "uuid": "%s"
            }
            ''' % self.campaign_id
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



    @httpretty.activate
    def test_update(self):
        """ Updating campaign """

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
