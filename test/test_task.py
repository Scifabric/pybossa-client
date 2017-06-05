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


class TestPybossaClientTask(TestPyBossaClient):
    @patch('pbclient.requests.delete')
    def test_delete_task(self, Mock):
        """Test delete_task works"""
        Mock.return_value = self.create_fake_request('', 204, 'text/html')
        res = self.client.delete_task(1)
        assert res is True, res

    @patch('pbclient.requests.get')
    def test_get_tasks(self, Mock):
        """Test get_tasks works"""
        Mock.return_value = self.create_fake_request([self.task.copy()], 200)
        res = self.client.get_tasks(1)
        assert len(res) == 1, len(res)
        task = res[0]
        assert task.id == self.task['id'], task
        assert task.project_id == self.task['project_id'], task

    @patch('pbclient.requests.get')
    def test_get_tasks_with_keyset_pagination(self, Mock):
        """Test get_tasks uses keyset pagination if a last_id argument is
        provided"""
        Mock.return_value = self.create_fake_request([], 200)
        self.client.get_tasks(1, last_id=1, limit=3)

        Mock.assert_called_once_with('http://localhost:5000/api/task',
                                     params={'api_key': 'tester',
                                             'project_id': 1,
                                             'limit': 3,
                                             'last_id': 1})

    @patch('pbclient.requests.get')
    def test_get_tasks_errors(self, Mock):
        """Test get tasks errors works"""
        targets = ['task']
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
                err = self.client.get_tasks(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_find_tasks(self, Mock):
        """Test find_tasks works"""
        Mock.return_value = self.create_fake_request([self.task.copy()], 200)
        res = self.client.find_tasks(project_id=1)
        assert len(res) == 1, len(res)
        task = res[0]
        assert task.id == self.task['id'], task
        assert task.project_id == self.task['project_id'], task

    @patch('pbclient.requests.get')
    def test_find_tasks_errors(self, Mock):
        """Test find task errors works"""
        targets = ['task']
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
                err = self.client.find_tasks(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.post')
    def test_create_task(self, Mock):
        """Test create_task works"""
        Mock.return_value = self.create_fake_request(self.task.copy(), 200)
        task = self.client.create_task(self.project['id'], self.task['info'])
        assert task.id == self.task['id'], task
        assert task.project_id == self.task['project_id'], task

    @patch('pbclient.requests.post')
    def test_create_task_errors(self, Mock):
        """Test create task errors works"""
        targets = ['task']
        errors = {'Unauthorized': 401, 'NotFound': 404, 'Forbidden': 401,
                  'TypeError': 415}
        for target in targets:
            for error in errors.keys():
                err_output = self.create_error_output(action='POST',
                                                      status_code=errors[error],
                                                      target=target,
                                                      exception_cls=error)
                Mock.return_value = self.create_fake_request(err_output,
                                                             errors[error])
                err = self.client.create_task(self.project['id'], self.task['info'])
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.put')
    def test_update_task(self, Mock):
        """Test update_task works"""
        Mock.return_value = self.create_fake_request(self.task, 200)
        task = self.client.update_task(pbclient.Task(self.task.copy()))
        assert task.id == self.task['id'], task
        assert task.project_id == self.task['project_id'], task

    @patch('pbclient.requests.put')
    def test_update_task_errors(self, Mock):
        """Test update task errors works"""
        targets = ['task']
        errors = {'Unauthorized': 401, 'NotFound': 404, 'Forbidden': 401,
                  'TypeError': 415, 'BadRequest': 400}
        for target in targets:
            for error in errors.keys():
                err_output = self.create_error_output(action='POST',
                                                      status_code=errors[error],
                                                      target=target,
                                                      exception_cls=error)
                Mock.return_value = self.create_fake_request(err_output,
                                                             errors[error])
                err = self.client.update_task(pbclient.Task(self.task.copy()))
                self.check_error_output(err_output, err)
