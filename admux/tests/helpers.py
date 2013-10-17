# coding: utf-8
import logging
log = logging.getLogger(__name__)

import functools

import httpretty

from adserver.client import Client


FAKE_REQUESTS = True

def fake_requests(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if FAKE_REQUESTS:
            httpretty.reset()
            httpretty.enable()
            try:
                return func(*args, **kwargs)
            finally:
                httpretty.disable()
        else:
            return func(*args, **kwargs)
    return wrapper


class BaseMixin(object):

    job_id = u"CA5434B0-1322-11E3-9E33-96237FA36B44"
