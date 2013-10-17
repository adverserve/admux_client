# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin

class OrdersMixin(object):
    order_id = None

    order_name = u"test-order"
    adition_id = 24
    agency_id = 25
    client_id = 26

    @fake_requests
    def _orders_list(self, *args, **kwargs):
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
        self.order_id = data['orders'][0]['uuid']

        return data

    @fake_requests
    def _order_create(self, *args, **kwargs):
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

        data = api.order_create(*args, **kwargs)
        self.order_id = data['order']

        return data

    @fake_requests
    def _order_delete(self, *args, **kwargs):
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

        self.order_id = None

        return api.order_delete(*args, **kwargs)



class OrdersTest(OrdersMixin, LoginMixin,
                 BaseMixin, TestCase):


    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._order_create(name=self.order_name)

    def tearDown(self):
        self._order_delete(self.order_id)

    @fake_requests
    def test_list(self):
        data = self._orders_list()
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
                "uuid": "%s",
                "width": 5
            }
            ''' % self.order_id
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
        data = self._order_delete(uuid=self.order_id)

        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])


    @fake_requests
    def test_create(self):
        data = self._order_create(name=self.order_name)
        self.assertTrue(u'order' in data)
        self.assertEquals(self.order_id, data[u'order'])

        self.assertTrue(u'job' in data)
        self.assertEquals(self.job_id, data[u'job'])

        data = self._order_create(name=self.order_name,

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

