# coding: utf-8
import httpretty

from ..context import Client

class CreativesMixin(object):
    creative_id = None

    creative_html = u'<p>Foo</p>'

    @httpretty.activate
    def _creatives_list(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "creatives": [
                    {
                        "active": null,
                        "adition_id": "2173210",
                        "clickwords": [
                            "http://admux-demo.trust-box.at/v1/clickwords/67C93426-359B-11E3-8E16-80D11002FE68"
                        ],
                        "created": "2013-10-15T13:12:11.000000",
                        "html": "\n                                    <div class=\"darkensite\">Hello World</div>\n",
                        "images": [],
                        "name": "Advertorial_kurier_advertorial",
                        "placement": "http://admux-demo.trust-box.at/v1/placements/94DA4392-0968-11E3-8AE3-B86E7401D844",
                        "updated": "2013-10-16T16:03:11.000000",
                        "uuid": "67323CB0-359B-11E3-8723-959B3BBECF3D"
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/campaigns/%s/creatives" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.creatives(uuid=self.campaign_id)
        self.creative_id = data['creatives'][0]['uuid']

        return data

    @httpretty.activate
    def _creative_delete(self, *args, **kwargs):
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
            Client.get_url("/creatives/%s" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        return api.creative_delete(uuid=self.creative_id)


    @httpretty.activate
    def _creative_create(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "creative" : "67323CB0-359B-11E3-8723-959B3BBECF3D",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/campaigns/%s/creatives" % self.campaign_id),
            body=body,
            content_type="application/json"
        )

        data = api.creative_create(*args, **kwargs)
        self.creative_id = data['creative']

        return data

