# -*- coding: utf8 -*-
# Copyright (C) 2017 Daniel Lombraña González
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


class TestPybossaClientHelpingMaterial(TestPyBossaClient):

    @patch('pbclient.requests.get')
    def test_get_helping_material(self, Mock):
        """Test get_helping_materials works."""
        Mock.return_value = self.create_fake_request([self.helping_material.copy()], 200)
        res = self.client.get_helping_materials(1)
        assert len(res) == 1, len(res)
        hm = res[0]
        assert hm.project_id == self.project['id'], hm

    @patch('pbclient.requests.get')
    def test_get_helping_materials_with_keyset_pagination(self, Mock):
        """Test get_helping_materials uses keyset pagination if a last_id argument is
        provided"""
        Mock.return_value = self.create_fake_request([], 200)
        self.client.get_helping_materials(1, last_id=1, limit=3)

        Mock.assert_called_once_with('http://localhost:5000/api/helpingmaterial',
                                     params={'api_key': 'tester',
                                             'project_id': 1,
                                             'limit': 3,
                                             'last_id': 1})

    @patch('pbclient.requests.get')
    def test_get_helping_materials_errors(self, Mock):
        """Test get helping materials errors works."""
        targets = ['helpingmaterial']
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
                err = self.client.get_helping_materials(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.get')
    def test_find_helping_materials(self, Mock):
        """Test find_helping_materials works"""
        Mock.return_value = self.create_fake_request([self.helping_material.copy()], 200)
        res = self.client.find_helping_materials(project_id=1)
        assert len(res) == 1, len(res)
        helping = res[0]
        assert helping.id == self.helping_material['id'], helping
        assert helping.project_id == self.helping_material['project_id'], helping
        assert helping.info == self.helping_material['info'], helping
        assert helping.media_url == self.helping_material['media_url'], helping

    @patch('pbclient.requests.get')
    def test_find_helping_materials_errors(self, Mock):
        """Test find helping materials errors works."""
        targets = ['helpingmaterial']
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
                err = self.client.find_helping_materials(1)
                self.check_error_output(err_output, err)

    @patch('pbclient.requests.put')
    def test_update_helping_material(self, Mock):
        """Test update_helping_material works"""
        Mock.return_value = self.create_fake_request(self.helping_material, 200)
        helping = self.client.update_helping_material(pbclient.Result(self.helping_material.copy()))
        assert helping.id == self.helping_material['id'], helping
        assert helping.project_id == self.helping_material['project_id'], helping
        assert helping.info == self.helping_material['info'], helping.info

    @patch('pbclient.requests.put')
    def test_update_helping_material_errors(self, Mock):
        """Test update helping_material errors works"""
        targets = ['helpingmaterial']
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
                err = self.client.update_helping_material(pbclient.Result(self.helping_material.copy()))
                self.check_error_output(err_output, err)
