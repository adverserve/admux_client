# coding: utf-8
import logging
log = logging.getLogger(__name__)

from datetime import datetime

import json
import httpretty
import unittest

from .context import Client, ProtocolClientError

from mixins.general import LoginMixin
from mixins.orders import OrdersMixin


class AddOrdersTest(OrdersMixin, LoginMixin,
                    unittest.TestCase):
    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

    def tearDown(self):
        try:
            self._order_delete(self.order_id)
        except ProtocolClientError:
            pass

    @httpretty.activate
    def test_create(self):
        """ Creating an Order """
        data = self._order_create(name=self.order_name)
        self.assertTrue(u'order' in data)
        self.assertEquals(self.order_id, data[u'order'])

        self.assertTrue(u'job' in data)



    @httpretty.activate
    def test_create_complex(self):
        """ Creating a complex Order """
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


class RemoveOrdersTest(OrdersMixin, LoginMixin,
                       unittest.TestCase):
    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

        data = self._order_create(name=self.order_name)


    @httpretty.activate
    def test_delete(self):
        """ Removing an Order """


        data = self._order_delete(uuid=self.order_id)

        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

        self.assertTrue(u'job' in data)


class OrdersTest(OrdersMixin, LoginMixin,
                 unittest.TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._order_create(name=self.order_name)

    def tearDown(self):
        self._order_delete(uuid=self.order_id)

    @httpretty.activate
    def test_list(self):
        """ Listing Orders """
        data = self._orders_list()
        self.assertTrue(u'orders' in data)


    @httpretty.activate
    def test_detail(self):
        """ Listing a single Order """
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


    @httpretty.activate
    def test_update(self):
        """ Updating an Order """
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

