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
from collections import namedtuple

FakeRequest = namedtuple('FakeRequest', ['text', 'status_code', 'headers'])


class TestPyBossaClient(object):
    project = dict(info='info',
               time_limit=0,
               description="description",
               short_name="slug",
               owner_id=1,
               category_id=1,
               id=1,
               link="<link rel='self' title='project' href='http://localhost:5000/api/project/1'/>",
               links=["<link rel='category' title='category' href='http://localhost:5000/api/category/1'/>"],
               allow_anonymous_contributors=True,
               hidden=0,
               long_description="long_description",
               name="test")

    category = dict(description="description",
                    short_name="slug",
                    id=1,
                    link="<link rel='self' title='category' href='http://localhost:5000/api/category/1'/>",
                    name="test")

    task = dict(info="info",
                n_answers=30,
                quorum=0,
                links=["<link rel='parent' title='project' href='http://localhost:5000/api/project/1'/>"],
                calibration=0,
                project_id=1,
                state="completed",
                link="<link rel='self' title='task' href='http://localhost:5000/api/task/1'/>",
                id=1)

    taskrun = dict(info="info",
                   user_id=None,
                   links=[
                       "<link rel='parent' title='project' href='http://localhost:5000/api/project/1'/>"
                       "<link rel='parent' title='task' href='http://localhost:5000/api/taskrun/1'/>"],
                   task_id=1,
                   calibration=None,
                   project_id=1,
                   user_ip="127.0.0.1",
                   link="<link rel='self' title='taskrun' href='http://localhost:5000/api/taskrun/1'/>",
                   id=1)

    result = dict(info=dict(foo='bar'),
                  created='today',
                  task_id=1,
                  project_id=1,
                  task_run_ids=[1],
                  last_version=True,
                  id=1)

    helping_material = dict(info=dict(key='value'),
                            created='today',
                            project_id=1,
                            media_url='/container/image.jpg',
                            id=1)


    def setUp(self):
        self.client = pbclient
        self.client.set('endpoint', 'http://localhost:5000')
        self.client.set('api_key', 'tester')

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
