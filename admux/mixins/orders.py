# coding: utf-8

from adserver.admux import helpers


class OrdersClientMixin(object):
    def orders(self, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/

        links: Boolean
        expand: array of strings
        """
        url = '/orders'
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def order(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/uuid/

        uuid: order identifier
        links: Boolean
        expand: array of strings
        """
        url = '/orders/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def order_delete(self, uuid):
        """
        http://admux-demo.trust-box.at/developer/api/v1/delete/orders/uuid/

        uuid: order identifier
        """
        url = '/orders/%(uuid)s' % { 'uuid': uuid, }
        return self._request('DELETE', url)

    def order_create(self, name,
                     adition_id=None, agency_id=None, client_id=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/post/orders/

        name: order name
        adition_id: optional numeric id
        agency_id: optional numeric id
        client_id: optional numeric id
        """
        url = '/orders'
        data = {
            u'name': name,
            u'adition_id': helpers._int(adition_id),
            u'agency_id': helpers._int(agency_id),
            u'client_id': helpers._int(client_id),
        }

        return self._request('POST', url, data=data)

    def order_update(self, uuid,
                     name=None,
                     adition_id=None, agency_id=None, client_id=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/put/orders/uuid/

        uuid: order identifier
        name: optional order name
        adition_id: optional numeric id
        agency_id: optional numeric id
        client_id: optional numeric id
        """
        url = '/orders/%(uuid)s' % { 'uuid': uuid, }
        data = {
            u'name': name,
            u'adition_id': helpers._int(adition_id),
            u'agency_id': helpers._int(agency_id),
            u'client_id': helpers._int(client_id),
        }

        return self._request('PUT', url, data=data)


