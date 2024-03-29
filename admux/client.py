# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import requests

from admux.mixins import websites, placements, orders, \
     campaigns, creatives, clickwords, images, jobs
from admux import helpers

class ProtocolError(Exception):
    pass

class ProtocolClientError(ProtocolError):
    pass

class ProtocolResourceError(ProtocolError):
    pass

class ProtocolPermissionError(ProtocolError):
    pass



class Client(websites.WebsitesClientMixin,
             placements.PlacementsClientMixin,
             orders.OrdersClientMixin,
             campaigns.CampaignsClientMixin,
             creatives.CreativesClientMixin,
             clickwords.ClickwordsClientMixin,
             images.ImagesClientMixin,
             jobs.JobsClientMixin):

    default_base_url = 'http://admux-demo.trust-box.at/v1'
    default_headers = {
        'content-type': 'application/json',
    }

    api_key = None

    @staticmethod
    def get_url(url):
        return '%s%s' % (Client.default_base_url, str(url))

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
            raise ProtocolClientError("API Key not set for client session. ' \
            'Try calling `login()` first.")
        if self.api_key:
            headers['Api-Key'] = self.api_key

        if params:
            params = helpers._clean_dict(params)

        if data:
            data = helpers._clean_dict(data)

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

        data = resp.json()
        if resp.status_code == 400:
            raise ProtocolClientError(data['error'])
        if resp.status_code == 403:
            raise ProtocolPermissionError(data['error'])
        if resp.status_code == 404:
            raise ProtocolResourceError(data['error'])

        resp.raise_for_status()
        return data

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


