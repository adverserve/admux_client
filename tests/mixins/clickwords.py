# coding: utf-8
from uuid import uuid4

import httpretty

from ..context import Client

class ClickwordsMixin(object):
    clickword_id = None

    clickword_tag = u'foobar-%s' % uuid4()
    clickword_url = u'http://foobar.com/some/path'

    @httpretty.activate
    def _clickwords_list(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "clickwords": [
                    {
                        "created": "2013-10-15T13:12:12.000000",
                        "tag": "wetter.at",
                        "updated": "2013-10-15T13:12:12.000000",
                        "url": "http://www.wetter.at",
                        "uuid": "6781F1CE-359B-11E3-B369-88EB2874B32D"
                    },
                    {
                        "created": "2013-10-15T13:12:12.000000",
                        "tag": "tennisnet.com",
                        "updated": "2013-10-15T13:12:12.000000",
                        "url": "http://www.tennisnet.com",
                        "uuid": "67C93426-359B-11E3-8E16-80D11002FE68"
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/creatives/%s/clickwords" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickwords(*args, **kwargs)
        self.clickword_id = data['clickwords'][0]['uuid']

        return data

    @httpretty.activate
    def _clickword_delete(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "message" : "Deleted",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/clickwords/%s" % self.clickword_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickword_delete(uuid=self.clickword_id)
        return data

    @httpretty.activate
    def _clickword_create(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "clickword" : "%s",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            ''' % self.clickword_id
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/creatives/%s/clickwords" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.clickword_create(*args, **kwargs)
        self.clickword_id = data['clickword']

        return data

