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


class TestPybossaClient:
    def setUp(self):
        self.client = pbclient
        self.client.set('endpoint', 'http://localhost:5000')
        self.client.set('api-key', 'tester')

    def test_00_get_app(self):
        """Test get_apps works"""
        # App does not exist should return 404 error object
        err = self.client.get_app(0)
        assert err['status'] == 'failed', err
        assert err['action'] == 'GET', err
        assert err['target'] == 'app', err
        assert err['exception_cls'] == 'NotFound', err
        assert err['status_code'] == 404, err
