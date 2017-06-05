# -*- coding: utf8 -*-
# Copyright (C) 2015 Daniel Lombraña González
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


class TestPybossaClientResult(TestPyBossaClient):

    @patch('pbclient.requests.get')
    def test_get_results(self, Mock):
        """Test get_results works."""
        Mock.return_value = self.create_fake_request([self.result.copy()], 200)
        res = self.client.get_results(1)
        assert len(res) == 1, len(res)
        result = res[0]
        assert result.id == self.task['id'], result
        assert result.project_id == self.task['project_id'], result

    @patch('pbclient.requests.get')
    def test_get_results_with_keyset_pagination(self, Mock):
        """Test get_results uses keyset pagination if a last_id argument is
        provided"""
        Mock.return_value = self.create_fake_request([], 200)
        self.client.get_results(1, last_id=1, limit=3)

        Mock.assert_called_once_with('http://localhost:5000/api/result',
                                     params={'api_key': 'tester',
                                             'project_id': 1,
                                             'limit': 3,
                                             'last_id': 1})

    @patch('pbclient.requests.get')
    def test_get_results_errors(self, Mock):
        """Test get results errors works."""
        targets = ['result']
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
                err = self.client.get_results(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_find_results(self, Mock):
        """Test find_results works"""
        Mock.return_value = self.create_fake_request([self.result.copy()], 200)
        res = self.client.find_results(project_id=1)
        assert len(res) == 1, len(res)
        result = res[0]
        assert result.id == self.result['id'], result
        assert result.project_id == self.result['project_id'], result
        assert result.task_id == self.result['task_id'], result
        assert result.task_run_ids == self.result['task_run_ids'], result

    @patch('pbclient.requests.get')
    def test_find_results_errors(self, Mock):
        """Test find results errors works."""
        targets = ['result']
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
                err = self.client.find_results(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.put')
    def test_update_result(self, Mock):
        """Test update_result works"""
        Mock.return_value = self.create_fake_request(self.result, 200)
        result = self.client.update_result(pbclient.Result(self.result.copy()))
        assert result.id == self.result['id'], result
        assert result.project_id == self.result['project_id'], result
        assert result.task_id == self.result['task_id'], result
        assert result.task_run_ids == self.result['task_run_ids'], result
        assert result.info == self.result['info'], result.info

    @patch('pbclient.requests.put')
    def test_update_result_errors(self, Mock):
        """Test update result errors works"""
        targets = ['result']
        errors = {'Unauthorized': 401, 'NotFound': 404, 'Forbidden': 401,
                  'TypeError': 415, 'BadRequest': 400}
        for target in targets:
            for error in errors.keys():
                err_output = self.create_error_output(action='PUT',
                                                      status_code=errors[error],
                                                      target=target,
                                                      exception_cls=error)
                Mock.return_value = self.create_fake_request(err_output,
                                                             errors[error])
                err = self.client.update_result(pbclient.Result(self.result.copy()))
                self.check_error_output(err_output, err)
