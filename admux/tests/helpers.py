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
    website_id = u"67D02286-0968-11E3-B1D1-9E6D76D7A1E6"
    placement_id = u"953E93A6-0968-11E3-877B-F091A39B799E"

    order_id = u"F01CD8A0-3596-11E3-8D31-B4305DD555A5"
    order_name = u"test-order"
    adition_id = 24
    agency_id = 25
    client_id = 26

    campaign_id = u"F0F9FFF0-3596-11E3-ABFF-E3E78741F450"
    campaign_name = u"test-campaign"
    campaign_type = u"closedClicks"
    invalid_campaign_type = u"invalid"

    creative_id = u"67323CB0-359B-11E3-8723-959B3BBECF3D"

    clickword_id = u"67C93426-359B-11E3-8E16-80D11002FE68"

    image_id = u"C9819C44-1322-11E3-9E33-96237FA36B44"

    job_id = u"CA5434B0-1322-11E3-9E33-96237FA36B44"
