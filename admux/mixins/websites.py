# coding: utf-8

import helpers


class WebsitesClientMixin(object):
    def websites(self, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/websites/

        links: Boolean
        expand: array of strings
        """
        url = '/websites'
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def website(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/websites/uuid/

        uuid: website identifier
        links: Boolean
        expand: array of strings
        """
        url = '/websites/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)


