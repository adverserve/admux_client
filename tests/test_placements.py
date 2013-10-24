# coding: utf-8
import logging
log = logging.getLogger(__name__)

import httpretty
import unittest

from .context import Client

from mixins.general import LoginMixin
from mixins.websites import WebsitesMixin
from mixins.placements import PlacementsMixin


class PlacementsTest(PlacementsMixin, WebsitesMixin, LoginMixin,
                     unittest.TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)
        self._get_websites()
        self._get_placements()

    @httpretty.activate
    def test_list(self):
        data = self._get_placements()
        self.assertTrue(u'placements' in data)


    @httpretty.activate
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
