# coding: utf-8

import helpers


class JobsClientMixin(object):
    def jobs(self, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/jobs/

        links: Boolean
        expand: array of strings (e.g. foobar)
        """
        url = '/jobs'
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def job(self, uuid, links=None, expand=None):
        """
        http://admux-demo.trust-box.at/developer/api/v1/get/jobs/uuid/

        uuid: job identifier
        links: Boolean
        expand: array of strings
        """
        url = '/jobs/%(uuid)s' % { 'uuid': uuid, }
        params = {
            'links': helpers._bool(links),
            'expand': helpers._list(expand),
        }

        return self._request('GET', url, params=params)

    def job_delete(self, uuid):
        """
        http://admux-demo.trust-box.at/developer/api/v1/delete/jobs/uuid/

        uuid: job identifier
        """
        url = '/jobs/%(uuid)s' % { 'uuid': uuid, }
        return self._request('DELETE', url)



