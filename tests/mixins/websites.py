# coding: utf-8
import httpretty

from ..context import Client

class WebsitesMixin(object):
    website_id = None

    @httpretty.activate
    def _get_websites(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "websites" : [
                   {
                      "name" : "Die Presse",
                      "uuid" : "C96A9030-1322-11E3-9E33-96237FA36B44",
                      "placements" : [
                         "http://admux-demo.trust-box.at/v1/placements/C96B4228-1322-11E3-9E33-96237FA36B44",
                         "http://admux-demo.trust-box.at/v1/placements/C96BE5DE-1322-11E3-9E33-96237FA36B44"
                      ],
                      "created" : "2013-09-01T16:23:08.000000Z",
                      "adition_id" : "816114",
                      "updated" : "2013-09-01T16:23:08.000000Z",
                      "advertorial_base_url" : "http://diepresse.at/advertorial/",
                      "links" : [
                         {
                            "rel" : "self",
                            "href" : "http://admux-demo.trust-box.at/v1/websites/C96A9030-1322-11E3-9E33-96237FA36B44"
                         }
                      ]
                   }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/websites"),
            body=body,
            content_type="application/json"
        )

        data = api.websites(*args, **kwargs)
        self.website_id = data['websites'][0]['uuid']

        return data
