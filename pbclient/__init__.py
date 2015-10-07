# -*- coding: utf-8 -*-
"""Dead simple pybossa client.

~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple PyBossa client

:license: MIT
"""

_opts = dict()

import requests
import json

OFFSET_WARNING = """
    INFO: you can use keyset pagination to get faster responses from the server.
    To learn more, please visit:
    https://github.com/PyBossa/pybossa-client#on-queries-and-performance
    """


def set(key, val):
    """Set key to value."""
    global _opts
    _opts[key] = val


def _pybossa_req(method, domain, id=None, payload=None, params={}):
    """
    Send a JSON request.

    Returns True if everything went well, otherwise it returns the status
    code of the response.
    """
    headers = {'content-type': 'application/json'}
    url = _opts['endpoint'] + '/api/' + domain
    if id is not None:
        url += '/' + str(id)
    if 'api_key' in _opts:
        params['api_key'] = _opts['api_key']
    if method == 'get':
        r = requests.get(url, params=params)
    elif method == 'post':
        r = requests.post(url, params=params, headers=headers,
                          data=json.dumps(payload))
    elif method == 'put':
        r = requests.put(url, params=params, headers=headers,
                         data=json.dumps(payload))
    elif method == 'delete':
        r = requests.delete(url, params=params, headers=headers,
                            data=json.dumps(payload))
    if r.status_code / 100 == 2:
        if r.text and r.text != '""':
            return json.loads(r.text)
        else:
            return True
    else:
        return json.loads(r.text)


class DomainObject(object):

    """Main Domain object Class."""

    def __init__(self, data):
        """Init method."""
        self.__dict__['data'] = data

    def __getattr__(self, name):
        """Get attribute."""
        data = self.__dict__['data']
        if name == 'data':
            return data
        if name in data:
            return data[name]
        raise AttributeError('unknown attribute: ' + name)

    def __setattr__(self, name, value):
        """Set attribute."""
        data = self.__dict__['data']
        if name == 'data':
            self.__dict__['data'] = value
            return True
        if name in data:
            data[name] = value
            return True
        raise AttributeError('unknown attribute: ' + name)


class Project(DomainObject):

    """Project class."""

    reserved_keys = dict(id=None, created=None, updated=None,
                         completed=None, contacted=None, published=None)

    def __repr__(self):  # pragma: no cover
        """Return a representation."""
        tmp = 'pybossa.Project("' + self.short_name + '", ' + str(self.id) + ')'
        return tmp


class Category(DomainObject):

    """Category class."""

    def __repr__(self):  # pragma: no cover
        """Return a representation."""
        tmp = ('pybossa.Category("' + self.short_name + '", '
               + str(self.id) + ')')
        return tmp


class Task(DomainObject):

    """Task Class."""

    reserved_keys = dict(id=None, created=None, state=None)

    def __repr__(self):  # pragma: no cover
        """Return a represenation."""
        return 'pybossa.Task(' + str(self.id) + ')'


class TaskRun(DomainObject):

    """Class TaskRun."""

    reserved_keys = dict(id=None, created=None, finish_time=None)

    def __repr__(self):  # pragma: no cover
        """Return representation."""
        return 'pybossa.TaskRun(' + str(self.id) + ')'


# Projects

def get_projects(limit=100, offset=0, last_id=None):
    """Return a list of registered projects.

    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :param last_id: id of the last project, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :rtype: list
    :returns: A list of PyBossa Projects

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        print OFFSET_WARNING
        params = dict(limit=limit, offset=offset)
    try:
        res = _pybossa_req('get', 'project',
                           params=params)
        if type(res).__name__ == 'list':
            return [Project(project) for project in res]
        else:
            raise TypeError
    except:  # pragma: no cover
        raise


def get_project(project_id):
    """Return a PyBossa Project for the project_id.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :rtype: PyBossa Project
    :returns: A PyBossa Project object

    """
    try:
        res = _pybossa_req('get', 'project', project_id)
        if res.get('id'):
            return Project(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def find_project(**kwargs):
    """Return a list with matching project arguments.

    :param kwargs: PyBossa Project members
    :rtype: list
    :returns: A list of projects that match the kwargs

    """
    try:
        res = _pybossa_req('get', 'project', params=kwargs)
        if type(res).__name__ == 'list':
            return [Project(project) for project in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def create_project(name, short_name, description):
    """Create a project.

    :param name: PyBossa Project Name
    :type name: string
    :param short_name: PyBossa Project short name or slug
    :type short_name: string
    :param description: PyBossa Project description
    :type decription: string
    :returns: True -- the response status code

    """
    try:
        project = dict(name=name, short_name=short_name,
                       description=description)
        res = _pybossa_req('post', 'project', payload=project)
        if res.get('id'):
            return Project(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def update_project(project):
    """Update a project instance.

    :param project: PyBossa project
    :type project: PyBossa Project
    :returns: True -- the response status code

    """
    try:
        project_id = project.id
        project = _forbidden_attributes(project)
        res = _pybossa_req('put', 'project', project_id, payload=project.data)
        if res.get('id'):
            return Project(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def delete_project(project_id):
    """Delete a Project with id = project_id.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('delete', 'project', project_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise


# Category

def get_categories(limit=20, offset=0, last_id=None):
    """Return a list of registered categories.

    :param limit: Number of returned items, default 20
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :param last_id: id of the last category, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :rtype: list
    :returns: A list of PyBossa Categories

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print OFFSET_WARNING
    try:
        res = _pybossa_req('get', 'category',
                           params=params)
        if type(res).__name__ == 'list':
            return [Category(category) for category in res]
        else:
            raise TypeError
    except:
        raise


def get_category(category_id):
    """Return a PyBossa Category for the category_id.

    :param category_id: PyBossa Category ID
    :type category_id: integer
    :rtype: PyBossa Category
    :returns: A PyBossa Category object

    """
    try:
        res = _pybossa_req('get', 'category', category_id)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def find_category(**kwargs):
    """Return a list with matching Category arguments.

    :param kwargs: PyBossa Category members
    :rtype: list
    :returns: A list of project that match the kwargs

    """
    try:
        res = _pybossa_req('get', 'category', params=kwargs)
        if type(res).__name__ == 'list':
            return [Category(category) for category in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def create_category(name, description):
    """Create a Category.

    :param name: PyBossa Category Name
    :type name: string
    :param description: PyBossa Category description
    :type decription: string
    :returns: True -- the response status code
    """
    try:
        category = dict(name=name, short_name=name.lower().replace(" ", ""),
                        description=description)
        res = _pybossa_req('post', 'category', payload=category)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def update_category(category):
    """Update a Category instance.

    :param category: PyBossa Category
    :type category: PyBossa Category
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('put', 'category',
                           category.id, payload=category.data)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def delete_category(category_id):
    """Delete a Category with id = category_id.

    :param category_id: PyBossa Category ID
    :type category_id: integer
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('delete', 'category', category_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise


# Tasks

def get_tasks(project_id, limit=100, offset=0, last_id=None):
    """Return a list of tasks for a given project ID.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :param last_id: id of the last task, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :type offset: integer
    :returns: True -- the response status code

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print OFFSET_WARNING
    params['project_id'] = project_id
    try:
        res = _pybossa_req('get', 'task',
                           params=params)
        if type(res).__name__ == 'list':
            return [Task(task) for task in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def find_tasks(project_id, **kwargs):
    """Return a list of matched tasks for a given project ID.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :param kwargs: PyBossa Task members
    :type info: dict
    :rtype: list
    :returns: A list of tasks that match the kwargs

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'task', params=kwargs)
        if type(res).__name__ == 'list':
            return [Task(task) for task in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def create_task(project_id, info, n_answers=30, priority_0=0, quorum=0):
    """Create a task for a given project ID.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :param info: PyBossa Project info JSON field
    :type info: dict
    :param n_answers: Number of answers or TaskRuns per task, default 30
    :type n_answers: integer
    :param priority_0: Value between 0 and 1 indicating priority of task within
        Project (higher = more important), default 0.0
    :type priority_0: float
    :param quorum: Number of times this task should be done by different users,
        default 0
    :type quorum: integer
    :returns: True -- the response status code
    """
    try:
        task = dict(
            project_id=project_id,
            info=info,
            calibration=0,
            priority_0=priority_0,
            n_answers=n_answers,
            quorum=quorum
        )
        res = _pybossa_req('post', 'task', payload=task)
        if res.get('id'):
            return Task(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def update_task(task):
    """Update a task for a given task ID.

    :param task: PyBossa task

    """
    try:
        task_id = task.id
        task = _forbidden_attributes(task)
        res = _pybossa_req('put', 'task', task_id, payload=task.data)
        if res.get('id'):
            return Task(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def delete_task(task_id):
    """Delete a task for a given task ID.

    :param task: PyBossa task

    """
    #: :arg task: A task
    try:
        res = _pybossa_req('delete', 'task', task_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise


# Task Runs

def get_taskruns(project_id, limit=100, offset=0, last_id=None):
    """Return a list of task runs for a given project ID.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :param last_id: id of the last taskrun, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :rtype: list
    :returns: A list of task runs for the given project ID

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print OFFSET_WARNING
    params['project_id'] = project_id
    try:
        res = _pybossa_req('get', 'taskrun',
                           params=params)
        if type(res).__name__ == 'list':
            return [TaskRun(taskrun) for taskrun in res]
        else:
            raise TypeError
    except:
        raise


def find_taskruns(project_id, **kwargs):
    """Return a list of matched task runs for a given project ID.

    :param project_id: PyBossa Project ID
    :type project_id: integer
    :param kwargs: PyBossa Task Run members
    :rtype: list
    :returns: A List of task runs that match the query members

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'taskrun', params=kwargs)
        if type(res).__name__ == 'list':
            return [TaskRun(taskrun) for taskrun in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def delete_taskrun(taskrun_id):
    """Delete the given taskrun.

    :param task: PyBossa task
    """
    try:
        res = _pybossa_req('delete', 'taskrun', taskrun_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise


def _forbidden_attributes(obj):
    """Return the object without the forbidden attributes."""
    for key in obj.data.keys():
        if key in obj.reserved_keys.keys():
            obj.data.pop(key)
    return obj
