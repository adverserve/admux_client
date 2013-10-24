# coding: utf-8
from uuid import uuid4

import httpretty

from ..context import Client

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
