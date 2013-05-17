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
    app = dict(info='info',
               time_limit=0,
               description="description",
               short_name="slug",
               owner_id=1,
               id=1,
               link="<link rel='self' title='app' href='http://localhost:5000/api/app/1'/>",
               allow_anonymous_contributors=True,
               hidden=0,
               long_description="long_description",
               name="test")

    task = dict(info="info",
                n_answers=30,
                quorum=0,
                links=["<link rel='parent' title='app' href='http://localhost:5000/api/app/1'/>"],
                calibration=0,
                app_id=1,
                state="completed",
                link="<link rel='self' title='task' href='http://localhost:5000/api/task/1'/>",
                id=1)

    taskrun = dict(info="info",
                   user_id=None,
                   links=[
                       "<link rel='parent' title='app' href='http://localhost:5000/api/app/1'/>"
                       "<link rel='parent' title='task' href='http://localhost:5000/api/taskrun/1'/>"],
                   task_id=1,
                   calibration=None,
                   app_id=1,
                   user_ip="127.0.0.1",
                   link="<link rel='self' title='taskrun' href='http://localhost:5000/api/taskrun/1'/>",
                   id=1)

    def setUp(self):
        self.client = pbclient
        self.client.set('endpoint', 'http://localhost:5000')
        self.client.set('api-key', 'tester')

    def create_fake_request(self, data, status=None, mimetype={'content-type': 'application/json'}):
        if status is None and data['status_code']:
            return FakeRequest(json.dumps(data), data['status_code'], mimetype)
        else:
            return FakeRequest(json.dumps(data), status, mimetype)

    def create_error_output(self, action, status_code, target,
                            exception_cls, exception_msg=None):
        error = dict(action=action,
                     status="failed",
                     status_code=status_code,
                     target=target,
                     exception_cls=exception_cls,
                     exception_msg=exception_msg)
        return error

    def check_error_output(self, res, err):
        for k in err.keys():
            assert err[k] == res[k], err

    @patch('pbclient.requests.get')
    def test_00_get_app_not_found(self, Mock):
        """Test get_app not found works"""
        # App does not exist should return 404 error object
        not_found = self.create_error_output(action='GET', status_code=404,
                                             target='app', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found)
        err = self.client.get_app(1)
        self.check_error_output(err, not_found)

    @patch('pbclient.requests.get')
    def test_01_get_app_found(self, Mock):
        """Test get_app found works"""
        Mock.return_value = self.create_fake_request(self.app, 200)
        app = self.client.get_app(1)
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

    @patch('pbclient.requests.get')
    def test_01_get_apps(self, Mock):
        """Test get_apps works"""
        Mock.return_value = self.create_fake_request([self.app], 200)
        apps = self.client.get_apps()
        assert len(apps) == 1, apps
        app = apps[0]
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

        # Without apps
        Mock.return_value = self.create_fake_request([], 200)
        apps = self.client.get_apps()
        assert len(apps) == 0, apps

    @patch('pbclient.requests.get')
    def test_02_find_app(self, Mock):
        """Test find_app works"""
        Mock.return_value = self.create_fake_request([self.app], 200)
        apps = self.client.find_app(short_name=self.app['short_name'])
        # Only one app is found
        assert len(apps) == 1, apps
        app = apps[0]
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

    @patch('pbclient.requests.get')
    def test_03_find_app_not_found(self, Mock):
        """Test find_app not found works"""
        Mock.return_value = self.create_fake_request([], 200)
        apps = self.client.find_app(short_name="foobar")
        assert len(apps) == 0, apps

    @patch('pbclient.requests.post')
    def test_04_create_app(self, Mock):
        """Test create_app works"""
        Mock.return_value = self.create_fake_request(self.app, 200)
        app = self.client.create_app(name=self.app['name'],
                                     short_name=self.app['short_name'],
                                     description=self.app['description'])
        assert app.id == self.app['id']
        assert app.short_name == self.app['short_name']

    @patch('pbclient.requests.post')
    def test_05_create_app_exists(self, Mock):
        """Test create_app duplicate entry works"""
        already_exists = self.create_error_output(action='POST', status_code=415,
                                                  target='app', exception_cls='IntegrityError')

        Mock.return_value = self.create_fake_request(already_exists, 415)
        app = self.client.create_app(name=self.app['name'],
                                     short_name=self.app['short_name'],
                                     description=self.app['description'])
        self.check_error_output(app, already_exists)

    @patch('pbclient.requests.post')
    def test_06_create_app_not_allowed(self, Mock):
        """Test create_app not authorized works"""
        not_authorized = self.create_error_output(action='POST', status_code=401,
                                                  target='app', exception_cls='Unauthorized')

        Mock.return_value = self.create_fake_request(not_authorized, 401)
        app = self.client.create_app(name=self.app['name'],
                                     short_name=self.app['short_name'],
                                     description=self.app['description'])
        self.check_error_output(app, not_authorized)

    @patch('pbclient.requests.post')
    def test_07_create_app_forbidden(self, Mock):
        """Test create_app not forbidden works"""
        forbidden = self.create_error_output(action='POST', status_code=403,
                                             target='app', exception_cls='Forbidden')

        Mock.return_value = self.create_fake_request(forbidden, 403)
        app = self.client.create_app(name=self.app['name'],
                                     short_name=self.app['short_name'],
                                     description=self.app['description'])
        self.check_error_output(app, forbidden)

    @patch('pbclient.requests.put')
    def test_08_update_app(self, Mock):
        """Test update_app works"""
        Mock.return_value = self.create_fake_request(self.app, 200)
        app = self.client.update_app(pbclient.App(self.app))
        assert app.id == self.app['id'], app
        assert app.short_name == self.app['short_name'], app

    @patch('pbclient.requests.put')
    def test_09_update_app_not_found(self, Mock):
        """Test update_app not found works"""
        not_found = self.create_error_output(action='PUT', status_code=404,
                                             target='app', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found, 404)
        err = self.client.update_app(pbclient.App(self.app))
        self.check_error_output(not_found, err)

    @patch('pbclient.requests.put')
    def test_10_update_app_forbidden(self, Mock):
        """Test update_app forbidden works"""
        forbidden = self.create_error_output(action='PUT', status_code=403,
                                             target='app', exception_cls='Forbidden')
        Mock.return_value = self.create_fake_request(forbidden, 403)
        err = self.client.update_app(pbclient.App(self.app))
        self.check_error_output(forbidden, err)

    @patch('pbclient.requests.put')
    def test_11_update_app_unauthorized(self, Mock):
        """Test update_app unauthorized works"""
        unauthorized = self.create_error_output(action='PUT', status_code=401,
                                                target='app', exception_cls='Unauthorized')
        Mock.return_value = self.create_fake_request(unauthorized, 401)
        err = self.client.update_app(pbclient.App(self.app))
        self.check_error_output(unauthorized, err)

    @patch('pbclient.requests.delete')
    def test_12_delete_app(self, Mock):
        """Test delete_app works"""
        Mock.return_value = self.create_fake_request('', 204, 'text/html')
        res = self.client.delete_app(1)
        assert res is True, res

    @patch('pbclient.requests.delete')
    def test_app_delete(self, Mock):
        """Test delete app errors works"""
        targets = ['app', 'task']
        errors = {'Unauthorized': 401, 'NotFound': 404, 'Forbidden': 401}
        for target in targets:
            for error in errors.keys():
                err_output = self.create_error_output(action='DELETE',
                                                      status_code=errors[error],
                                                      target=target,
                                                      exception_cls=error)
                Mock.return_value = self.create_fake_request(err_output,
                                                             errors[error])
                if target == 'app':
                    err = self.client.delete_app(1)
                if target == 'task':
                    err = self.client.delete_task(1)
                self.check_error_output(err_output, err)
