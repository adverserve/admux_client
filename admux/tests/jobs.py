# coding: utf-8
import logging
log = logging.getLogger(__name__)

import json
import httpretty

from django.test import TestCase

from adserver.client import Client
from adserver.tests.helpers import BaseMixin, fake_requests
from adserver.tests.general import LoginMixin

class JobsTest(BaseMixin, LoginMixin, TestCase):

    def setUp(self):
        self.api = Client()
        self._login(*self.credentials)

    @fake_requests
    def test_list(self):
        body = r'' \
            r'''
            {
                "jobs" : [
                    {
                        "status" : "todo",
                        "args" : {
                            "created" : "2013-09-01 16:23:09",
                            "name" : "New order",
                            "agency_id" : 43,
                            "user_id" : 2,
                            "updated" : "2013-09-01 16:23:09",
                            "id" : 9,
                            "uuid" : "CA538F42-1322-11E3-9E33-96237FA36B44"
                        },
                        "uuid" : "CA5434B0-1322-11E3-9E33-96237FA36B44",
                        "created" : "2013-09-01T16:23:09.000000Z",
                        "worker" : "InsertOrder",
                        "updated" : "2013-09-01T16:23:09.000000Z",
                        "links" : [
                                {
                                    "rel" : "self",
                                    "href" : "http://admux-demo.trust-box.at/v1/jobs/CA5434B0-1322-11E3-9E33-96237FA36B44"
                                }
                            ],
                        "result" : null
                    }
                ]
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/jobs"),
            body=body,
            content_type="application/json"
        )

        data = api.jobs()
        self.assertTrue(u'jobs' in data)

        data = api.jobs(links=True, expand=[ u'foo', ])
        self.assertTrue(u'jobs' in data)

        if httpretty.httpretty.is_enabled():
            self.assertEqual(httpretty.last_request().querystring,
                             { u'links': [ u'1', ],
                               u'expand': [ u'foo', ] })


    @fake_requests
    def test_detail(self):
        body = r'' \
            r'''
            {
                "status" : "todo",
                "args" : {
                    "created" : "2013-09-01 16:23:09",
                    "name" : "New order",
                    "agency_id" : 43,
                    "user_id" : 2,
                    "updated" : "2013-09-01 16:23:09",
                    "id" : 9,
                    "uuid" : "CA538F42-1322-11E3-9E33-96237FA36B44"
                },
                "uuid" : "CA5434B0-1322-11E3-9E33-96237FA36B44",
                "created" : "2013-09-01T16:23:09.000000Z",
                "worker" : "InsertOrder",
                "updated" : "2013-09-01T16:23:09.000000Z",
                "links" : [
                        {
                            "rel" : "self",
                            "href" : "http://admux-demo.trust-box.at/v1/jobs/CA5434B0-1322-11E3-9E33-96237FA36B44"
                        }
                    ],
                "result" : null
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.GET,
            Client.get_url("/jobs/%s" % self.job_id),
            body=body,
            content_type="application/json"
        )

        data = api.job(uuid=self.job_id)
        self.assertTrue(u'uuid' in data)
        self.assertEqual(self.job_id, data[u'uuid'])

        data = api.job(uuid=self.job_id, links=True, expand=[ u'foo', ])
        self.assertTrue(u'uuid' in data)


    @fake_requests
    def test_delete(self):
        body = r'' \
            r'''
            {
                "message" : "Deleted"
            }
            '''
        api = self.api

        httpretty.register_uri(
            httpretty.DELETE,
            Client.get_url("/jobs/%s" % self.job_id),
            body=body,
            content_type="application/json"
        )

        data = api.job_delete(uuid=self.job_id)
        self.assertTrue(u'message' in data)
        self.assertEquals(u'Deleted', data[u'message'])

