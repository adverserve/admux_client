# coding: utf-8
import httpretty

from ..context import Client

class PlacementsMixin(object):
    placement_id = None

    @httpretty.activate
    def _get_placements(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "placements": [
                    {
                        "adition_id": "2566638",
                        "created": "2013-08-20T07:17:33.000000",
                        "height": 5,
                        "name": "kurier_sport_advertorial",
                        "type": "teaser",
                        "updated": "2013-08-20T07:17:33.000000",
                        "uuid": "953E93A6-0968-11E3-877B-F091A39B799E",
                        "width": 5
                    }
                ]
            }
        '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/websites/%s/placements" % self.website_id),
            body=body,
            content_type="application/json"
        )

        data = api.placements(uuid=self.website_id)
        self.placement_id = data['placements'][0]['uuid']

        return data
