# -*- coding: utf8 -*-
# Copyright (C) 2013 Daniel Lombraña González
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pbclient
import json
from mock import patch
from collections import namedtuple

FakeRequest = namedtuple('FakeRequest', ['text', 'status_code', 'headers'])


class TestPybossaClient(object):

    def setUp(self):
        self.client = pbclient
        self.client.set('endpoint', 'http://localhost:5000')
        self.client.set('api-key', 'tester')

    def create_fake_request(self, data, status=None, mimetype={'content-type': 'application/json'}):
        if status is None and data['status_code']:
            return FakeRequest(json.dumps(data), data['status_code'], mimetype)

    def create_error_output(self, action, status_code, target,
                            exception_cls, exception_msg=None):
        error = dict(action=action,
                     status="failed",
                     status_code=status_code,
                     target=target,
                     exception_cls=exception_cls,
                     exception_msg=exception_msg)
        return error

    @patch('pbclient.requests.get')
    def test_00_get_app_not_found(self, Mock):
        """Test get_app not found works"""
        # App does not exist should return 404 error object
        not_found = self.create_error_output(action='GET', status_code=404,
                                             target='app', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found)
        err = self.client.get_app(0)
        assert err['status'] == 'failed', err
        assert err['action'] == 'GET', err
        assert err['target'] == 'app', err
        assert err['exception_cls'] == 'NotFound', err
        assert err['status_code'] == 404, err
