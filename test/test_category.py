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
from mock import patch
from base import TestPyBossaClient


class TestPybossaClientCategory(TestPyBossaClient):
    @patch('pbclient.requests.get')
    def test_00_get_category_not_found(self, Mock):
        """Test get category not found works"""
        # App does not exist should return 404 error object
        not_found = self.create_error_output(action='GET', status_code=404,
                                             target='app', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found)
        err = self.client.get_category(1)
        self.check_error_output(err, not_found)

    @patch('pbclient.requests.get')
    def test_01_get_category_found(self, Mock):
        """Test get category found works"""
        Mock.return_value = self.create_fake_request(self.app, 200)
        app = self.client.get_category(1)
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

    @patch('pbclient.requests.get')
    def test_get_category_errors(self, Mock):
        """Test get app errors works"""
        targets = ['app']
        errors = {'Unauthorized': 401, 'NotFound': 404, 'Forbidden': 401,
                  'TypeError': 415}
        for target in targets:
            for error in errors.keys():
                err_output = self.create_error_output(action='GET',
                                                      status_code=errors[error],
                                                      target=target,
                                                      exception_cls=error)
                Mock.return_value = self.create_fake_request(err_output,
                                                             errors[error])
                err = self.client.get_category(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_01_get_categories(self, Mock):
        """Test get_categories works"""
        Mock.return_value = self.create_fake_request([self.app], 200)
        apps = self.client.get_categories()
        assert len(apps) == 1, apps
        app = apps[0]
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

        # Without apps
        Mock.return_value = self.create_fake_request([], 200)
        apps = self.client.get_categories()
        assert len(apps) == 0, apps

    @patch('pbclient.requests.get')
    def test_02_find_category(self, Mock):
        """Test find_category works"""
        Mock.return_value = self.create_fake_request([self.app], 200)
        apps = self.client.find_category(short_name=self.app['short_name'])
        # Only one app is found
        assert len(apps) == 1, apps
        app = apps[0]
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

    @patch('pbclient.requests.get')
    def test_find_category_errors(self, Mock):
        """Test find app errors works"""
        targets = ['app']
        errors = {'Unauthorized': 401, 'NotFound': 404, 'Forbidden': 401,
                  'TypeError': 415}
        for target in targets:
            for error in errors.keys():
                err_output = self.create_error_output(action='GET',
                                                      status_code=errors[error],
                                                      target=target,
                                                      exception_cls=error)
                Mock.return_value = self.create_fake_request(err_output,
                                                             errors[error])
                err = self.client.find_category(short_name=self.app['short_name'])
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_03_find_category_not_found(self, Mock):
        """Test find_category not found works"""
        Mock.return_value = self.create_fake_request([], 200)
        apps = self.client.find_category(short_name="foobar")
        assert len(apps) == 0, apps

    @patch('pbclient.requests.post')
    def test_04_create_category(self, Mock):
        """Test create_category works"""
        Mock.return_value = self.create_fake_request(self.app, 200)
        app = self.client.create_category(name=self.app['name'],
                                          description=self.app['description'])
        assert app.id == self.app['id']
        assert app.short_name == self.app['short_name']

    @patch('pbclient.requests.post')
    def test_05_create_category_exists(self, Mock):
        """Test create_category duplicate entry works"""
        already_exists = self.create_error_output(action='POST', status_code=415,
                                                  target='app', exception_cls='IntegrityError')

        Mock.return_value = self.create_fake_request(already_exists, 415)
        app = self.client.create_category(name=self.app['name'],
                                          description=self.app['description'])
        self.check_error_output(app, already_exists)

    @patch('pbclient.requests.post')
    def test_06_create_category_not_allowed(self, Mock):
        """Test create_category not authorized works"""
        not_authorized = self.create_error_output(action='POST', status_code=401,
                                                  target='app', exception_cls='Unauthorized')

        Mock.return_value = self.create_fake_request(not_authorized, 401)
        app = self.client.create_category(name=self.app['name'],
                                          description=self.app['description'])
        self.check_error_output(app, not_authorized)

    @patch('pbclient.requests.post')
    def test_07_create_category_forbidden(self, Mock):
        """Test create_category not forbidden works"""
        forbidden = self.create_error_output(action='POST', status_code=403,
                                             target='app', exception_cls='Forbidden')

        Mock.return_value = self.create_fake_request(forbidden, 403)
        app = self.client.create_category(name=self.app['name'],
                                          description=self.app['description'])
        self.check_error_output(app, forbidden)

    @patch('pbclient.requests.put')
    def test_08_update_category(self, Mock):
        """Test update_category works"""
        Mock.return_value = self.create_fake_request(self.app, 200)
        app = self.client.update_category(pbclient.App(self.app))
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

    @patch('pbclient.requests.put')
    def test_09_update_category_not_found(self, Mock):
        """Test update_category not found works"""
        not_found = self.create_error_output(action='PUT', status_code=404,
                                             target='app', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found, 404)
        err = self.client.update_category(pbclient.App(self.app))
        self.check_error_output(not_found, err)

    @patch('pbclient.requests.put')
    def test_10_update_category_forbidden(self, Mock):
        """Test update_category forbidden works"""
        forbidden = self.create_error_output(action='PUT', status_code=403,
                                             target='app', exception_cls='Forbidden')
        Mock.return_value = self.create_fake_request(forbidden, 403)
        err = self.client.update_category(pbclient.App(self.app))
        self.check_error_output(forbidden, err)

    @patch('pbclient.requests.put')
    def test_11_update_category_unauthorized(self, Mock):
        """Test update_category unauthorized works"""
        unauthorized = self.create_error_output(action='PUT', status_code=401,
                                                target='app', exception_cls='Unauthorized')
        Mock.return_value = self.create_fake_request(unauthorized, 401)
        err = self.client.update_category(pbclient.App(self.app))
        self.check_error_output(unauthorized, err)

    @patch('pbclient.requests.delete')
    def test_12_delete_category(self, Mock):
        """Test delete_category works"""
        Mock.return_value = self.create_fake_request('', 204, 'text/html')
        res = self.client.delete_category(1)
        assert res is True, res