# coding: utf-8
from uuid import uuid4

import httpretty

from ..context import Client

class OrdersMixin(object):
    order_id = None

    order_name = u"demo-order-%s" % uuid4()
    adition_id = 24
    agency_id = 25
    client_id = 26

    @httpretty.activate
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

    @httpretty.activate
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

    @httpretty.activate
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

