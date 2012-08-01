#
# Dead simple pybossa client
#

_opts = dict()

import requests
import json


def set(key, val):
    global _opts
    _opts[key] = val


def _pybossa_req(method, domain, id=None, payload=None, params=None):
    """
    Sends a JSON request
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
    if r.text:
        result = json.loads(r.text)
    else:
        result = r.status_code
    return result


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
        return 'pybossa.App("' + self.short_name + '")'


class Task(DomainObject):
    def __repr__(self):
        return 'pybossa.Task("' + self.id + '")'


def get_apps():
    return [App(app_data) for app_data in _pybossa_req('get', 'app')]


def get_app(app_id):
    return App(_pybossa_req('get', 'app', app_id))


def find_app(**kwargs):
    return [App(app_data) for app_data in _pybossa_req('get', 'app', params=kwargs)]


def update_app(app):
    _pybossa_req('put', 'app', app.id, payload=app.data)


def delete_app(app_id):
    pass


def get_tasks(app_id, limit=100):
    return [Task(task_data) for task_data in _pybossa_req('get', 'task', params=dict(app_id=app_id, limit=limit))]


def find_tasks(app_id, **kwargs):
    kwargs['app_id'] = app_id
    return [Task(task_data) for task_data in _pybossa_req('get', 'task', params=kwargs)]


def create_task(app_id, info):
    task = dict(app_id=app_id, state=0, calibration=0, priority_0=0, info=info)
    _pybossa_req('post', 'task', payload=task)


def update_task(task):
    _pybossa_req('put', 'task', task.id, payload=task.data)


def delete_task(task):
    status = _pybossa_req('delete', 'task', task.id, payload=dict(app_id=task.app_id))
    if status >= 300:
        status = 'status: %d' % status
        print 'could not delete task', task.id, '(%s)' % status
