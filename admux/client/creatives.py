# coding: utf-8

from adserver.client import helpers


class CreativesClientMixin(object):
    def creatives(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/campaigns/uuid/creatives/

        uuid: campaign identifier
        links: Boolean
        expand: array of strings (e.g. clickwords,images)
        """
        url = '/campaigns/%(uuid)s/creatives' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def creative(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/uuid/

        uuid: creative identifier
        links: Boolean
        expand: array of strings (e.g. clickwords,images)
        """
        url = '/creatives/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

