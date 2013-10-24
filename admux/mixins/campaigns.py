# coding: utf-8

import helpers


class CampaignsClientMixin(object):

    def campaigns(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/orders/uuid/campaigns/

        uuid: order identifier
        links: Boolean
        expand: array of strings (e.g. creatives,clickwords)
        """
        url = '/orders/%(uuid)s/campaigns' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
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
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def campaign_delete(self, uuid):
        """
        http://admux-demo.trust-box.at/developer/api/v1/delete/campaigns/uuid/

        uuid: campaign identifier
        """
        url = '/campaigns/%(uuid)s' % { 'uuid': uuid, }
        return self._request('DELETE', url)

    def campaign_create(self, uuid, name,
                        adition_id=None, campaign_type=None, total=None,
                        priority=None, from_runtime=None, to_runtime=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/post/orders/uuid/campaigns/

        uuid: order identifier
        name: campaign name

        adition_id: optional numeric id
        campaign_type: string. Valid options: [ closedClicks,
                                                closedViews,
                                                open,
                                                redirect ]
        total: optional numeric id
        priority: optional numeric id
        from_runtime: optional datetime. Format: 2013-08-23T08:00:00
        to_runtime: optional datetime. Format: 2013-10-05T20:15:00
        """
        url = '/orders/%(uuid)s/campaigns' % { 'uuid': uuid, }

        data = {
            u'name': name,
            u'adition_id': helpers._int(adition_id),
            u'campaign_type': helpers._in_list(campaign_type, [ u'closedClicks',
                                                                u'closedViews',
                                                                u'open',
                                                                u'redirect', ]),
            u'total': helpers._int(total),
            u'prioriry': helpers._int(priority),
            u'from_runtime': helpers._datetime(from_runtime),
            u'to_runtime': helpers._datetime(to_runtime),
        }

        return self._request('POST', url, data=data)

    def campaign_update(self, uuid,
                        name=None,
                        adition_id=None, campaign_type=None, total=None,
                        priority=None, from_runtime=None, to_runtime=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/put/campaigns/uuid/

        uuid: order identifier
        name: optional order name
        adition_id: optional numeric id
        campaign_type: string. Valid options: [ closedClicks,
                                                closedViews,
                                                open,
                                                redirect ]
        total: optional numeric id
        priority: optional numeric id
        from_runtime: optional datetime. Format: 2013-08-23T08:00:00
        to_runtime: optional datetime. Format: 2013-10-05T20:15:00
        """
        url = '/campaigns/%(uuid)s' % { 'uuid': uuid, }
        data = {
            u'name': name,
            u'adition_id': helpers._int(adition_id),
            u'campaign_type': helpers._in_list(campaign_type, [ u'closedClicks',
                                                                u'closedViews',
                                                                u'open',
                                                                u'redirect', ]),
            u'total': helpers._int(total),
            u'prioriry': helpers._int(priority),
            u'from_runtime': helpers._datetime(from_runtime),
            u'to_runtime': helpers._datetime(to_runtime),
        }

        return self._request('PUT', url, data=data)
