# coding: utf-8

import helpers


class ClickwordsClientMixin(object):
    def clickwords(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/creatives/uuid/clickwords/

        uuid: creative identifier
        links: Boolean
        expand: array of strings (e.g. foobar)
        """
        url = '/creatives/%(uuid)s/clickwords' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def clickword(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/clickwords/uuid/

        uuid: clickword identifier
        links: Boolean
        expand: array of strings (e.g. clickwords,images)
        """
        url = '/clickwords/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def clickword_delete(self, uuid):
        """
        http://admux-demo.trust-box.at/developer/api/v1/delete/clickwords/uuid/

        uuid: clickword identifier
        """
        url = '/clickwords/%(uuid)s' % { 'uuid': uuid, }
        return self._request('DELETE', url)

    def clickword_create(self, uuid, tag, url):
        """
        http://admux-demo.trust-box.at/developer/api/v1/post/creatives/uuid/clickwords/

        uuid: creative identifier
        tag: clickword tag
        url: e.g. http://foobar.com/some/path
        """
        url = '/creatives/%(uuid)s/clickwords' % { 'uuid': uuid, }
        data = {
            u'tag': tag,
            u'url': url,
        }

        return self._request('POST', url, data=data)

    def clickword_update(self, uuid,
                         tag=None, url=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/put/creatives/uuid/

        uuid: clickword identifier
        tag: optional clickword tag
        url: optional e.g. http://foobar.com/some/path
        """
        url = '/clickwords/%(uuid)s' % { 'uuid': uuid, }
        data = {
            u'tag': tag,
            u'url': url,
        }

        return self._request('PUT', url, data=data)


