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
from nose.tools import assert_raises


class TestPybossaClientProject(TestPyBossaClient):

    @patch('pbclient.requests.get')
    def test_get_project_not_found(self, Mock):
        """Test get_project not found works"""
        # Project does not exist should return 404 error object
        pbclient.set('endpoint', 'http://localhost')
        pbclient.set('api_key', 'key')
        not_found = self.create_error_output(action='GET', status_code=404,
                                             target='project', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found)
        err = self.client.get_project(1)
        self.check_error_output(err, not_found)

    @patch('pbclient.requests.get')
    def test_get_project_found(self, Mock):
        """Test get_project found works"""
        Mock.return_value = self.create_fake_request(self.project, 200)
        project = self.client.get_project(1)
        assert project.id == self.project['id'], project
        assert project.short_name == self.project['short_name'], project

    @patch('pbclient.requests.get')
    def test_get_project_errors(self, Mock):
        """Test get project errors works"""
        targets = ['project']
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
                err = self.client.get_project(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_get_projects(self, Mock):
        """Test get_projects works"""
        Mock.return_value = self.create_fake_request([self.project], 200)
        projects = self.client.get_projects()
        assert len(projects) == 1, projects
        project = projects[0]
        assert project.id == self.project['id'], project
        assert project.short_name == self.project['short_name'], project

        # Without projects
        Mock.return_value = self.create_fake_request([], 200)
        projects = self.client.get_projects()
        assert len(projects) == 0, projects

    @patch('pbclient.requests.get')
    def test_get_projects_with_keyset_pagination(self, Mock):
        """Test get_projects uses keyset pagination if a last_id argument is
        provided"""
        Mock.return_value = self.create_fake_request([], 200)
        self.client.get_projects(last_id=1, limit=3)

        Mock.assert_called_once_with('http://localhost:5000/api/project',
                                     params={'limit': 3,
                                             'last_id': 1,
                                             'api_key': 'tester'})

    @patch('pbclient.requests.get')
    def test_get_projects_raises_error_if_not_list(self, Mock):
        """Test get_projects only accepts lists of projects from the server"""
        Mock.return_value = self.create_fake_request(self.project, 200)
        assert_raises(TypeError, self.client.get_projects)

    @patch('pbclient.requests.get')
    def test_find_project(self, Mock):
        """Test find_project works"""
        Mock.return_value = self.create_fake_request([self.project], 200)
        projects = self.client.find_project(short_name=self.project['short_name'])
        # Only one project is found
        assert len(projects) == 1, projects
        project = projects[0]
        assert project.id == self.project['id'], project
        assert project.short_name == self.project['short_name'], project

    @patch('pbclient.requests.get')
    def test_find_project_errors(self, Mock):
        """Test find project errors works"""
        targets = ['project']
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
                err = self.client.find_project(short_name=self.project['short_name'])
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_find_project_not_found(self, Mock):
        """Test find_project not found works"""
        Mock.return_value = self.create_fake_request([], 200)
        projects = self.client.find_project(short_name="foobar")
        assert len(projects) == 0, projects

    @patch('pbclient.requests.post')
    def test_create_project(self, Mock):
        """Test create_project works"""
        Mock.return_value = self.create_fake_request(self.project, 200)
        project = self.client.create_project(name=self.project['name'],
                                     short_name=self.project['short_name'],
                                     description=self.project['description'])
        assert project.id == self.project['id']
        assert project.short_name == self.project['short_name']

    @patch('pbclient.requests.post')
    def test_create_project_exists(self, Mock):
        """Test create_project duplicate entry works"""
        already_exists = self.create_error_output(action='POST', status_code=415,
                                                  target='project', exception_cls='IntegrityError')

        Mock.return_value = self.create_fake_request(already_exists, 415)
        project = self.client.create_project(name=self.project['name'],
                                     short_name=self.project['short_name'],
                                     description=self.project['description'])
        self.check_error_output(project, already_exists)

    @patch('pbclient.requests.post')
    def test_create_project_not_allowed(self, Mock):
        """Test create_project not authorized works"""
        not_authorized = self.create_error_output(action='POST', status_code=401,
                                                  target='project', exception_cls='Unauthorized')

        Mock.return_value = self.create_fake_request(not_authorized, 401)
        project = self.client.create_project(name=self.project['name'],
                                     short_name=self.project['short_name'],
                                     description=self.project['description'])
        self.check_error_output(project, not_authorized)

    @patch('pbclient.requests.post')
    def test_create_project_forbidden(self, Mock):
        """Test create_project not forbidden works"""
        forbidden = self.create_error_output(action='POST', status_code=403,
                                             target='project', exception_cls='Forbidden')

        Mock.return_value = self.create_fake_request(forbidden, 403)
        project = self.client.create_project(name=self.project['name'],
                                     short_name=self.project['short_name'],
                                     description=self.project['description'])
        self.check_error_output(project, forbidden)

    @patch('pbclient.requests.put')
    def test_update_project(self, Mock):
        """Test update_project works"""
        Mock.return_value = self.create_fake_request(self.project, 200)
        project = pbclient.Project(self.project.copy())
        u_project = self.client.update_project(project)
        assert u_project.id == self.project['id'], project
        assert u_project.short_name == self.project['short_name'], project

    @patch('pbclient.requests.put')
    def test_update_project_400(self, Mock):
        """Test update_project does not allow reserved attributes works"""
        bad_request= self.create_error_output(action='PUT',
                                              status_code=400,
                                              target='project',
                                              exception_cls='BadRequest')
        Mock.return_value = self.create_fake_request(bad_request, 400)
        err = self.client.update_project(pbclient.Project(self.project.copy()))
        self.check_error_output(bad_request, err)

    @patch('pbclient.requests.put')
    def test_update_project_not_found(self, Mock):
        """Test update_project not found works"""
        not_found = self.create_error_output(action='PUT', status_code=404,
                                             target='project', exception_cls='NotFound')
        Mock.return_value = self.create_fake_request(not_found, 404)
        err = self.client.update_project(pbclient.Project(self.project.copy()))
        self.check_error_output(not_found, err)

    @patch('pbclient.requests.put')
    def test_update_project_forbidden(self, Mock):
        """Test update_project forbidden works"""
        forbidden = self.create_error_output(action='PUT', status_code=403,
                                             target='project', exception_cls='Forbidden')
        Mock.return_value = self.create_fake_request(forbidden, 403)
        project = pbclient.Project(self.project.copy())
        err = self.client.update_project(project)
        self.check_error_output(forbidden, err)

    @patch('pbclient.requests.put')
    def test_update_project_unauthorized(self, Mock):
        """Test update_project unauthorized works"""
        unauthorized = self.create_error_output(action='PUT', status_code=401,
                                                target='project', exception_cls='Unauthorized')
        Mock.return_value = self.create_fake_request(unauthorized, 401)
        project = pbclient.Project(self.project.copy())
        err = self.client.update_project(project)
        self.check_error_output(unauthorized, err)

    @patch('pbclient.requests.delete')
    def test_delete_project(self, Mock):
        """Test delete_project works"""
        Mock.return_value = self.create_fake_request('', 204, 'text/html')
        res = self.client.delete_project(1)
        assert res is True, res
