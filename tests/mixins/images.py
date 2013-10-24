# coding: utf-8
import httpretty

from ..context import Client

class ImagesMixin(object):
    image_id = None

    @httpretty.activate
    def _images_list(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "images": [
                    {
                       "created" : "2013-09-01T16:23:08.000000Z",
                       "filename" : "erdbeere.jpg",
                       "data" : "/9j/[..]KAUB//2Q==\n",
                       "updated" : "2013-09-01T16:23:08.000000Z",
                       "uuid" : "C9819C44-1322-11E3-9E33-96237FA36B44",
                       "links" : [
                          {
                             "rel" : "self",
                             "href" : "http://admux-demo.trust-box.at/v1/images/C9819C44-1322-11E3-9E33-96237FA36B44"
                          },
                          {
                             "rel" : "up",
                             "href" : "http://admux-demo.trust-box.at/v1/creatives/C97FA33A-1322-11E3-9E33-96237FA36B44"
                          }
                       ]
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/creatives/%s/images" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.images(*args, **kwargs)
        self.image_id = data['images'][0]['uuid']

        return data

    @httpretty.activate
    def _image_delete(self, *args, **kwargs):
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
            Client.get_url("/images/%s" % self.image_id),
            body=body,
            content_type="application/json"
        )

        data = api.image_delete(*args, **kwargs)
        return data

    @httpretty.activate
    def _image_create(self, *args, **kwargs):
        body = r'' \
            r'''
            {
                "image" : "C9819C44-1322-11E3-9E33-96237FA36B44",
                "job" : "CA5434B0-1322-11E3-9E33-96237FA36B44"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.POST,
            Client.get_url("/creatives/%s/images" % self.creative_id),
            body=body,
            content_type="application/json"
        )

        data = api.image_create(*args, **kwargs)
        self.image_id = data['image']

        return data
