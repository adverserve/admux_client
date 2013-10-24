#!/usr/bin/env python
# coding:utf-8
import logging
log = logging.getLogger(__name__)

import requests
from pprint import pprint

from admux.client import Client

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