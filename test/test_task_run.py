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

from mock import patch
from base import TestPyBossaClient


class TestPybossaClientTaskRun(TestPyBossaClient):
    @patch('pbclient.requests.delete')
    def test_app_task_taskrun_delete(self, Mock):
        """Test delete app, task and taskrun errors works"""
        targets = ['app', 'task', 'taskrun']
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
                if target == 'taskrun':
                    err = self.client.delete_task(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_get_taskruns(self, Mock):
        """Test get_taskruns works"""
        Mock.return_value = self.create_fake_request([self.taskrun], 200)
        res = self.client.get_tasks(1)
        assert len(res) == 1, len(res)
        taskrun = res[0]
        assert taskrun.id == self.taskrun['id'], taskrun
        assert taskrun.app_id == self.taskrun['app_id'], taskrun

    @patch('pbclient.requests.get')
    def test_find_taskruns(self, Mock):
        """Test find_taskruns works"""
        Mock.return_value = self.create_fake_request([self.taskrun], 200)
        res = self.client.find_taskruns(app_id=1)
        assert len(res) == 1, len(res)
        taskrun = res[0]
        assert taskrun.id == self.taskrun['id'], taskrun
        assert taskrun.app_id == self.taskrun['app_id'], taskrun

    @patch('pbclient.requests.get')
    def test_find_taskruns_errors(self, Mock):
        """Test find taskruns errors works"""
        targets = ['taskrun']
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
                err = self.client.find_taskruns(1)
                self.check_error_output(err_output, err)
