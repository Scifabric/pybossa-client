# -*- coding: utf-8 -*-
"""
    Dead simple pybossa client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    A simple PyBossa client

    :license: MIT
"""

_opts = dict()

import requests
import json


def set(key, val):
    global _opts
    _opts[key] = val


def _pybossa_req(method, domain, id=None, payload=None, params=None):
    """
    Sends a JSON request

    Returns True if everything went well, otherwise it returns the status code of the response
    """
    headers = {'content-type': 'application/json'}
    url = _opts['endpoint'] + '/api/' + domain
    if id is not None:
        url += '/' + str(id)
    if params is None:
        params = dict()
    if 'api_key' in _opts:
        params['api_key'] = _opts['api_key']
    if method == 'get':
        r = requests.get(url, params=params)
    elif method == 'post':
        r = requests.post(url, params=params, headers=headers, data=json.dumps(payload))
    elif method == 'put':
        r = requests.put(url, params=params, headers=headers, data=json.dumps(payload))
    elif method == 'delete':
        r = requests.delete(url, params=params, headers=headers, data=json.dumps(payload))
    #print r.status_code, r.status_code / 100
    if r.status_code / 100 == 2:
        if r.text and r.text != '""':
            return json.loads(r.text)
        else:
            return True
    else:
        return json.loads(r.text)


# app
class DomainObject(object):

    def __init__(self, data):
        self.__dict__['data'] = data

    def __getattr__(self, name):
        data = self.__dict__['data']
        if name == 'data':
            return data
        if name in data:
            return data[name]
        raise AttributeError('unknown attribute: ' + name)

    def __setattr__(self, name, value):
        data = self.__dict__['data']
        if name == 'data':
            self.__dict__['data'] = value
            return True
        if name in data:
            data[name] = value
            return True
        raise AttributeError('unknown attribute: ' + name)


class App(DomainObject):
    def __repr__(self):
        return 'pybossa.App("' + self.short_name + '", ' + str(self.id) + ')'


class Category(DomainObject):
    def __repr__(self):
        return 'pybossa.Category("' + self.short_name + '", ' + str(self.id) + ')'


class Task(DomainObject):
    def __repr__(self):
        return 'pybossa.Task(' + str(self.id) + ')'


class TaskRun(DomainObject):
    def __repr__(self):
        return 'pybossa.TaskRun(' + str(self.id) + ')'


# Apps

def get_apps(limit=100, offset=0):
    """Returns a list of registered apps

    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer

    :rtype: list
    :returns: A list of PyBossa Applications

    """
    try:
        res = _pybossa_req('get', 'app', params=dict(limit=limit, offset=offset))
        if type(res).__name__ == 'list':
            return [App(app) for app in res]
        else:
            return res
    except:
        raise


def get_app(app_id):
    """Returns a PyBossa Application for the app_id

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :rtype: PyBossa Application
    :returns: A PyBossa Application object

    """
    try:
        res = _pybossa_req('get', 'app', app_id)
        if res.get('id'):
            return App(res)
        else:
            return res
    except:
        raise


def find_app(**kwargs):
    """Returns a list with matching app arguments

    :param kwargs: PyBossa Application members
    :rtype: list
    :returns: A list of application that match the kwargs

    """
    try:
        res = _pybossa_req('get', 'app', params=kwargs)
        if type(res).__name__ == 'list':
            return [App(app) for app in res]
        else:
            return res
    except:
        raise


def create_app(name, short_name, description):
    """Creates an application

    :param name: PyBossa Application Name
    :type name: string
    :param short_name: PyBossa Application short name or slug
    :type short_name: string
    :param description: PyBossa Application description
    :type decription: string
    :returns: True -- the response status code


    """
    try:
        app = dict(name=name, short_name=short_name, description=description)
        res = _pybossa_req('post', 'app', payload=app)
        if res.get('id'):
            return App(res)
        else:
            return res
    except:
        raise


def update_app(app):
    """Updates an application app instance

    :param app: PyBossa Application
    :type app: PyBossa Application
    :returns: True -- the response status code


    """
    try:
        res = _pybossa_req('put', 'app', app.id, payload=app.data)
        if res.get('id'):
            return App(res)
        else:
            return res
    except:
        raise


def delete_app(app_id):
    """Deletes an Application with id = app_id

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('delete', 'app', app_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:
        raise

# Category


def get_categories(limit=20, offset=0):
    """Returns a list of registered categories

    :param limit: Number of returned items, default 20
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer

    :rtype: list
    :returns: A list of PyBossa Categories

    """
    try:
        res = _pybossa_req('get', 'category', params=dict(limit=limit, offset=offset))
        if type(res).__name__ == 'list':
            return [Category(category) for category in res]
        else:
            return res
    except:
        raise


def get_category(category_id):
    """Returns a PyBossa Category for the category_id

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
    except:
        raise


def find_category(**kwargs):
    """Returns a list with matching Category arguments

    :param kwargs: PyBossa Category members
    :rtype: list
    :returns: A list of application that match the kwargs

    """
    try:
        res = _pybossa_req('get', 'category', params=kwargs)
        if type(res).__name__ == 'list':
            return [Category(category) for category in res]
        else:
            return res
    except:
        raise


def create_category(name, description):
    """Creates a Category

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
    except:
        raise


def update_category(category):
    """Updates a Category instance

    :param app: PyBossa Category
    :type app: PyBossa Category
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('put', 'category', category.id, payload=category.data)
        if res.get('id'):
            return Category(res)
        else:
            return res
    except:
        raise


def delete_category(category_id):
    """Deletes a Category with id = category_id

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
    except:
        raise


# Tasks

def get_tasks(app_id, limit=100, offset=0):
    """Returns a list of tasks for a given application ID

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :returns: True -- the response status code

    """
    try:
        res = _pybossa_req('get', 'task',
                           params=dict(app_id=app_id, limit=limit, offset=offset))
        if type(res).__name__ == 'list':
            return [Task(task) for task in res]
        else:
            return res
    except:
        raise


def find_tasks(app_id, **kwargs):
    """Returns a list of matched tasks for a given application ID

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :param kwargs: PyBossa Task members
    :type info: dict
    :rtype: list
    :returns: A list of tasks that match the kwargs

    """

    try:
        kwargs['app_id'] = app_id
        res = _pybossa_req('get', 'task', params=kwargs)
        if type(res).__name__ == 'list':
            return [Task(task) for task in res]
        else:
            return res
    except:
        raise


def create_task(app_id, info, n_answers=30, priority_0=0, quorum=0):
    """Creates a task for a given application ID

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :param info: PyBossa Application info JSON field
    :type info: dict
    :param n_answers: Number of answers or TaskRuns per task, default 30
    :type n_answers: integer
    :param priority_0: Value between 0 and 1 indicating priority of task within App (higher = more important), default 0.0
    :type priority_0: float
    :param quorum: Number of times this task should be done by different users, default 0
    :type quorum: integer
    :returns: True -- the response status code
    """
    try:
        task = dict(
            app_id=app_id,
            info=info,
            state=0,
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
    except:
        raise


def update_task(task):
    """Updates a task for a given task ID

    :param task: PyBossa task

    """
    try:
        res = _pybossa_req('put', 'task', task.id, payload=task.data)
        if res.get('id'):
            return Task(res)
        else:
            return res
    except:
        raise


def delete_task(task_id):
    """Deletes a task for a given task ID

    :param task: PyBossa task

    """
    #: :arg task: A task
    try:
        res = _pybossa_req('delete', 'task', task_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:
        raise


# Task Runs

def get_taskruns(app_id, limit=100, offset=0):
    """Returns a list of task runs for a given application ID

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :param limit: Number of returned items, default 100
    :type limit: integer
    :param offset: Offset for the query, default 0
    :type offset: integer
    :rtype: list
    :returns: A list of task runs for the given application ID

    """
    try:
        res = _pybossa_req('get', 'taskrun',
                           params=dict(app_id=app_id, limit=limit, offset=offset))
        if type(res).__name__ == 'list':
            return [TaskRun(taskrun) for taskrun in res]
        else:
            return res
    except:
        raise


def find_taskruns(app_id, **kwargs):
    """Returns a list of matched task runs for a given application ID

    :param app_id: PyBossa Application ID
    :type app_id: integer
    :param kwargs: PyBossa Task Run members
    :rtype: list
    :returns: A List of task runs that match the query members

    """
    try:
        kwargs['app_id'] = app_id
        res = _pybossa_req('get', 'taskrun', params=kwargs)
        if type(res).__name__ == 'list':
            return [TaskRun(taskrun) for taskrun in res]
        else:
            return res
    except:
        raise


def delete_taskrun(taskrun_id):
    """Deletes the given taskrun

    :param task: PyBossa task
    """
    try:
        res = _pybossa_req('delete', 'taskrun', taskrun_id)
        if type(res).__name__ == 'bool':
            return True
        else:
            return res
    except:
        raise
