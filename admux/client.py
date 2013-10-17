# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import requests
from pprint import pprint


class ProtocolError(Exception):
    pass

class Client(object):
    default_base_url = 'http://admux-demo.trust-box.at/v1'
    default_headers = {
        'content-type': 'application/json',
    }

    api_key = None

    @staticmethod
    def get_url(url):
        return '%s%s' % (Client.default_base_url, str(url))

    # Argument-Helpers
    @staticmethod
    def _list(values):
        if values:
            values = ",".join(values)
        return values

    @staticmethod
    def _int(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _bool(val):
        if val:
            return 1
        return None

    @staticmethod
    def _clean_dict(dictionary):
        return filter(lambda x: x[1] is not None, dictionary.items())

    # Request-Wrapper
    def _request(self,
                 method, url,
                 requires_api_key=True,
                 params=None, data=None, headers=None,
                 *args, **kwargs):

        absolute_url = Client.get_url(url)

        headers = dict(headers or {})
        headers.update(self.default_headers)

        if requires_api_key and not self.api_key:
            raise ProtocolError("API Key not set for client session. ' \
            'Try calling `login()` first.")
        if self.api_key:
            headers['Api-Key'] = self.api_key

        if params:
            params = Client._clean_dict(params)

        if data:
            # converting to json
            data = json.dumps(data)

        log.info("Adserver-Request: %s, %s", absolute_url, params)

        resp = requests.request(method, absolute_url,
                                params=params,
                                data=data,
                                headers=headers,
                                *args, **kwargs)

        log.info("Adserver-Response: %s, (%s)",
                 resp.status_code,
                 resp.text)

        resp.raise_for_status()
        return resp.json()

    # Login
    # =====
    def login(self, username, password):
        """
        http://admux-demo.trust-box.at/developer/api/v1/post/login/

        username: Username
        password: Password

        returns the api_key for given login-credentials
        (also sets the api_key as an internal variable)
        """

        data = self._request('POST', '/login', data={
            'username' : username,
            'password' : password,
        }, requires_api_key=False)

        self.api_key = data['api_key']

        return self.api_key


    # Websites
    # ========
    def websites(self, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/websites/

        links: Boolean
        expand: array of strings
        """
        url = '/websites'
        params = {
            'links': Client._bool(links),
            'expand': Client._list(expand),
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
            'links': Client._bool(links),
            'expand': Client._list(expand),
        }

        return self._request('GET', url, params=params)


    # Placements
    # ==========
    def placements(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/websites/uuid/placements/

        uuid: website identifier
        links: Boolean
        expand: array of strings
        """
        url = '/websites/%(uuid)s/placements' % { 'uuid': uuid, }
        params = {
            'links': Client._bool(links),
            'expand': Client._list(expand),
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
            'links': Client._bool(links),
            'expand': Client._list(expand),
        }

        return self._request('GET', url, params=params)


    # Orders
    # ======
    def orders(self, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/

        links: Boolean
        expand: array of strings
        """
        url = '/orders'
        params = {
            'links': Client._bool(links),
            'expand': Client._list(expand),
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
            'links': Client._bool(links),
            'expand': Client._list(expand),
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
            u'adition_id': Client._int(adition_id),
            u'agency_id': Client._int(agency_id),
            u'client_id': Client._int(client_id),
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
            u'adition_id': Client._int(adition_id),
            u'agency_id': Client._int(agency_id),
            u'client_id': Client._int(client_id),
        }

        return self._request('PUT', url, data=data)


    # Campaigns
    # ======
    def campaigns(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/uuid/campaigns/

        uuid: order identifier
        links: Boolean
        expand: array of strings (e.g. creatives,clickwords)
        """
        url = '/orders/%(uuid)s/campaigns' % { 'uuid': uuid, }
        params = {
            'links': Client._bool(links),
            'expand': Client._list(expand),
        }

        return self._request('GET', url, params=params)

    def campaign(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/uuid/

        uuid: campaign identifier
        links: Boolean
        expand: array of strings (e.g. creatives,clickwords)
        """
        url = '/campaigns/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': Client._bool(links),
            'expand': Client._list(expand),
        }

        return self._request('GET', url, params=params)



if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)
    log.addHandler(ch)

    log.setLevel(logging.DEBUG)

    c = Client()
    try:
        c.login(username='strg', password='strg')

        data = c.websites()

        website_uuid = data.get('websites', [ {}, ])[0].get('uuid')
        pprint(c.placement("953E93A6-0968-11E3-877B-F091A39B799E"))

    except requests.exceptions.HTTPError, e:
        log.error('Request failed.')