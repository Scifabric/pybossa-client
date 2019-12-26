# -*- coding: utf-8 -*-
"""Dead simple pybossa client.

~~~~~~~~~~~~~~~~~~~~~~~~~~

A simple PYBOSSA client

:license: MIT
"""


import requests
import json


_opts = dict()


OFFSET_WARNING = """
    INFO: you can use keyset pagination to get faster responses from the server.
    To learn more, please visit:
    https://github.com/PYBOSSA/pybossa-client#on-queries-and-performance
    """


def set(key, val):
    """Set key to value."""
    global _opts
    _opts[key] = val


def _pybossa_req(method, domain, id=None, payload=None, params={},
                 headers={'content-type': 'application/json'},
                 files=None):
    """
    Send a JSON request.

    Returns True if everything went well, otherwise it returns the status
    code of the response.
    """
    url = _opts['endpoint'] + '/api/' + domain
    if id is not None:
        url += '/' + str(id)
    if 'api_key' in _opts:
        params['api_key'] = _opts['api_key']
    if method == 'get':
        r = requests.get(url, params=params)
    elif method == 'post':
        if files is None and headers['content-type'] == 'application/json':
            r = requests.post(url, params=params, headers=headers,
                              data=json.dumps(payload))
        else:
            r = requests.post(url, params=params, files=files, data=payload)
    elif method == 'put':
        r = requests.put(url, params=params, headers=headers,
                         data=json.dumps(payload))
    elif method == 'delete':
        r = requests.delete(url, params=params, headers=headers,
                            data=json.dumps(payload))
    if r.status_code // 100 == 2:
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
                         completed=None, contacted=None, published=None,
                         secret_key=None)

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

    reserved_keys = dict(id=None, created=None, state=None,
                         fav_user_ids=None)

    def __repr__(self):  # pragma: no cover
        """Return a represenation."""
        return 'pybossa.Task(' + str(self.id) + ')'


class TaskRun(DomainObject):

    """Class TaskRun."""

    reserved_keys = dict(id=None, created=None, finish_time=None)

    def __repr__(self):  # pragma: no cover
        """Return representation."""
        return 'pybossa.TaskRun(' + str(self.id) + ')'


class Result(DomainObject):

    """Class Result."""

    reserved_keys = dict(id=None, created=None, project_id=None,
                         task_id=None, task_run_ids=None, last_version=None)

    def __repr__(self):  # pragma: no cover
        """Return representation."""
        return 'pybossa.Result(' + str(self.id) + ')'


class HelpingMaterial(DomainObject):

    """Class HelpingMaterial."""

    reserved_keys = dict(id=None, created=None)

    def __repr__(self):  # pragma: no cover
        """Return representation."""
        return 'pybossa.HelpingMaterial(' + str(self.id) + ')'


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
    :returns: A list of PYBOSSA Projects

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        print(OFFSET_WARNING)
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
    """Return a PYBOSSA Project for the project_id.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :rtype: PYBOSSA Project
    :returns: A PYBOSSA Project object

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

    :param kwargs: PYBOSSA Project members
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

    :param name: PYBOSSA Project Name
    :type name: string
    :param short_name: PYBOSSA Project short name or slug
    :type short_name: string
    :param description: PYBOSSA Project description
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

    :param project: PYBOSSA project
    :type project: PYBOSSA Project
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

    :param project_id: PYBOSSA Project ID
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
    :returns: A list of PYBOSSA Categories

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print(OFFSET_WARNING)
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
    """Return a PYBOSSA Category for the category_id.

    :param category_id: PYBOSSA Category ID
    :type category_id: integer
    :rtype: PYBOSSA Category
    :returns: A PYBOSSA Category object

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

    :param kwargs: PYBOSSA Category members
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

    :param name: PYBOSSA Category Name
    :type name: string
    :param description: PYBOSSA Category description
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

    :param category: PYBOSSA Category
    :type category: PYBOSSA Category
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

    :param category_id: PYBOSSA Category ID
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

    :param project_id: PYBOSSA Project ID
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
        print(OFFSET_WARNING)
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

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA Task members
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

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param info: PYBOSSA Project info JSON field
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

    :param task: PYBOSSA task

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

    :param task: PYBOSSA task

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

    :param project_id: PYBOSSA Project ID
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
        print(OFFSET_WARNING)
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

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA Task Run members
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

    :param task: PYBOSSA task
    """
    try:
        res = _pybossa_req('delete', 'taskrun', taskrun_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:  # pragma: no cover
        raise


# Results

def get_results(project_id, limit=100, offset=0, last_id=None):
    """Return a list of results for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :param last_id: id of the last result, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :type offset: integer
    :returns: True -- the response status code

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print(OFFSET_WARNING)
    params['project_id'] = project_id
    try:
        res = _pybossa_req('get', 'result',
                           params=params)
        if type(res).__name__ == 'list':
            return [Result(result) for result in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def find_results(project_id, **kwargs):
    """Return a list of matched results for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA Results members
    :type info: dict
    :rtype: list
    :returns: A list of results that match the kwargs

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'result', params=kwargs)
        if type(res).__name__ == 'list':
            return [Result(result) for result in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def update_result(result):
    """Update a result for a given result ID.

    :param result: PYBOSSA result

    """
    try:
        result_id = result.id
        result = _forbidden_attributes(result)
        res = _pybossa_req('put', 'result', result_id, payload=result.data)
        if res.get('id'):
            return Result(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def _forbidden_attributes(obj):
    """Return the object without the forbidden attributes."""
    for key in list(obj.data.keys()):
        if key in list(obj.reserved_keys.keys()):
            obj.data.pop(key)
    return obj


# Helping Material


def create_helpingmaterial(project_id, info, media_url=None, file_path=None):
    """Create a helping material for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param info: PYBOSSA Helping Material info JSON field
    :type info: dict
    :param media_url: URL for a media file (image, video or audio)
    :type media_url: string
    :param file_path: File path to the local image, video or sound to upload. 
    :type file_path: string
    :returns: True -- the response status code
    """
    try:
        helping = dict(
            project_id=project_id,
            info=info,
            media_url=None,
        )
        if file_path:
            files = {'file': open(file_path, 'rb')}
            payload = {'project_id': project_id}
            res = _pybossa_req('post', 'helpingmaterial',
                               payload=payload, files=files)
        else:
            res = _pybossa_req('post', 'helpingmaterial', payload=helping)
        if res.get('id'):
            return HelpingMaterial(res)
        else:
            return res
    except:  # pragma: no cover
        raise


def get_helping_materials(project_id, limit=100, offset=0, last_id=None):
    """Return a list of helping materials for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :param last_id: id of the last helping material, used for pagination. If provided, offset is ignored
    :type last_id: integer
    :type offset: integer
    :returns: True -- the response status code

    """
    if last_id is not None:
        params = dict(limit=limit, last_id=last_id)
    else:
        params = dict(limit=limit, offset=offset)
        print(OFFSET_WARNING)
    params['project_id'] = project_id
    try:
        res = _pybossa_req('get', 'helpingmaterial',
                           params=params)
        if type(res).__name__ == 'list':
            return [HelpingMaterial(helping) for helping in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def find_helping_materials(project_id, **kwargs):
    """Return a list of matched helping materials for a given project ID.

    :param project_id: PYBOSSA Project ID
    :type project_id: integer
    :param kwargs: PYBOSSA HelpingMaterial members
    :type info: dict
    :rtype: list
    :returns: A list of helping materials that match the kwargs

    """
    try:
        kwargs['project_id'] = project_id
        res = _pybossa_req('get', 'helpingmaterial', params=kwargs)
        if type(res).__name__ == 'list':
            return [HelpingMaterial(helping) for helping in res]
        else:
            return res
    except:  # pragma: no cover
        raise


def update_helping_material(helpingmaterial):
    """Update a helping material for a given helping material ID.

    :param helpingmaterial: PYBOSSA helping material

    """
    try:
        helpingmaterial_id = helpingmaterial.id
        helpingmaterial = _forbidden_attributes(helpingmaterial)
        res = _pybossa_req('put', 'helpingmaterial',
                           helpingmaterial_id, payload=helpingmaterial.data)
        if res.get('id'):
            return HelpingMaterial(res)
        else:
            return res
    except:  # pragma: no cover
        raise
