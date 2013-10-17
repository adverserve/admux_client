# coding: utf-8

from adserver.client import helpers


class ImagesClientMixin(object):
    def images(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/creatives/uuid/images/

        uuid: creative identifier
        links: Boolean
        expand: array of strings (e.g. foobar)
        """
        url = '/creatives/%(uuid)s/images' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def image(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/clickwords/uuid/

        uuid: image identifier
        links: Boolean
        expand: array of strings (e.g. clickwords,images)
        """
        url = '/images/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def image_delete(self, uuid):
        """
        http://admux-demo.trust-box.at/developer/api/v1/delete/images/uuid/

        uuid: clickword identifier
        """
        url = '/images/%(uuid)s' % { 'uuid': uuid, }
        return self._request('DELETE', url)

    def image_create(self, uuid, file_name, file_object=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/post/creatives/uuid/images/

        uuid: creative identifier
        file_name: string (path to file)
        file_object: optional file-object with binary read-permissions
        """
        url = '/creatives/%(uuid)s/images' % { 'uuid': uuid, }

        data = {}
        data.update(helpers._file(file_name, file_object))

        return self._request('POST', url, data=data)

    def image_update(self, uuid, file_name=None, file_object=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/put/images/uuid/

        uuid: image identifier
        file_name: optional string (path to file)
        file_object: optional file-object with binary read-permissions
        """
        url = '/images/%(uuid)s' % { 'uuid': uuid, }

        data = {}
        data.update(helpers._file(file_name, file_object))

        return self._request('PUT', url, data=data)


