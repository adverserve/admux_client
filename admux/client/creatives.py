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

    def creative_delete(self, uuid):
        """
        http://admux-demo.trust-box.at/developer/api/v1/delete/creatives/uuid/

        uuid: creative identifier
        """
        url = '/creatives/%(uuid)s' % { 'uuid': uuid, }
        return self._request('DELETE', url)

    def creative_create(self, uuid, html, placement):
        """
        http://admux-demo.trust-box.at/developer/api/v1/post/campaigns/uuid/creatives/

        uuid: campaign identifier
        html: creative name
        placement: placement identifier
        """
        url = '/campaigns/%(uuid)s/creatives' % { 'uuid': uuid, }
        data = {
            u'html': html,
            u'placement': placement,
        }

        return self._request('POST', url, data=data)

    def creative_update(self, uuid,
                        html=None, placement=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/put/creatives/uuid/

        uuid: creative identifier
        html: optional html code
        placement: optional placement identifier
        """
        url = '/creatives/%(uuid)s' % { 'uuid': uuid, }
        data = {
            u'html': html,
            u'placement': placement,
        }

        return self._request('PUT', url, data=data)


