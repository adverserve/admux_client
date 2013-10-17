# coding: utf-8
import logging
log = logging.getLogger(__name__)

import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin
from adserver.tests.websites import WebsiteMixin

class PlacementsMixin(object):
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

class PlacementsTest(PlacementsMixin, WebsiteMixin, LoginMixin,
                     BaseMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._get_websites()
        self._get_placements()

    @fake_requests
    def test_list(self):
        data = self._get_placements()
        self.assertTrue(u'placements' in data)


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
            ''' % self.placement_id
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/placements/%s" % self.placement_id),
            body=body,
            content_type="application/json"
        )

        data = api.placement(uuid=self.placement_id)
        self.assertTrue(u'uuid' in data)
        self.assertEquals(self.placement_id, data[u'uuid'])
