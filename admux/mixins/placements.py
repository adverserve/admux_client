# coding: utf-8

from admux import helpers


class PlacementsClientMixin(object):
    def placements(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/websites/uuid/placements/

        uuid: website identifier
        links: Boolean
        expand: array of strings
        """
        url = '/websites/%(uuid)s/placements' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def placement(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/placements/uuid/

        uuid: placement identifier
        links: Boolean
        expand: array of strings
        """
        url = '/placements/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)


