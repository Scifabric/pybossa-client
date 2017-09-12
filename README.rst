.. image:: https://travis-ci.org/Scifabric/pybossa-client.png
   :target: https://travis-ci.org/#!/Scifabric/pybossa-client
.. image:: https://img.shields.io/pypi/v/pybossa-client.svg
   :target: https://pypi.python.org/pypi/pybossa-client
.. image:: https://img.shields.io/pypi/dm/pybossa-client.svg
   :target: https://pypi.python.org/pypi/pybossa-client
.. image:: https://img.shields.io/badge/python-2.7-green.svg
   :target: https://pypi.python.org/pypi/pybossa-client
.. image:: https://img.shields.io/badge/python-3.5-blue.svg
   :target: https://pypi.python.org/pypi/pybossa-client
.. image:: https://img.shields.io/badge/python-3.6-orange.svg
   :target: https://pypi.python.org/pypi/pybossa-client


Dead simple Python client for PYBOSSA
=====================================

Makes it easy to work with `PYBOSSA <http://pybossa.com>`_

Requirements
------------

`PYBOSSA Server <http://pybossa.com>`_ >= 1.2.0.

Install
-------

You can install pybossa-client using **pip**, preferably while working in a 
`virtualenv <http://www.virtualenv.org/en/latest/index.html>`_::

    $ pip install pybossa-client 

Usage
-----

Setup::

    >>> import pbclient

    # setup the server connection
    >>> pbclient.set('endpoint', 'http://pybossa.com')
    >>> pbclient.set('api_key', '--your-api-key-here--')

Query a PYBOSSA server::

    >>> pbclient.get_projects()

    [pybossa.Project("project1", 1), pybossa.Project("project2", 2),
    pybossa.Project("project3", 3), pybossa.Project("project4", 4),
    pybossa.Project("project5", 5), pybossa.Project("project6", 6),
    pybossa.Project("project7", 7), pybossa.Project("project8", 8)]

    >>> pbclient.get_tasks(1)
    # tasks for project with id=1

    [pybossa.Task("Task1", 1), pybossa.Task("Task2", 2),
    pybossa.Task("Task3", 3), pybossa.Task("Task4", 4),
    pybossa.Task("Task5", 5), pybossa.Task("Task6", 6)]

Create a project::

    >>> pbclient.create_project('Name of the Project', 'shortname', 'Description')

Change the long description of a project::

    >>> project = pbclient.find_project(short_name='flickrperson')[0]
    >>> project.long_description = open('longdesc.html').read()
    
    >>> pbclient.update_project(project)

Replace the task presenter template::

    >>> project = pbclient.find_project(short_name='flickrperson')[0]
    >>> project.info['task_presenter'] = open('presenter.html').read()
    
    >>> pbclient.update_project(project)

Create a new task::

    >>> task_info = {
        'image': 'http://farm9.staticflickr.com/8146/7566819662_f2c74e77d8_m.jpg'
    }
    >>> pbclient.create_task(project_id, task_info)

Create a new helping material::

    >>> helping_info = {
        'key': 'value'
    }
    >>> pbclient.create_task(project_id, helping_info)

    >>> helping_info = {
        'project_id': project_id
    }
    >>> files: {'file': open('/tmp/img.jpg', 'rb')}
    >>> hm = pbclient.create_helpingmaterial(project_id, helping_info, files=files)
    >>> print hm.media_url
    /uploads/container/img.jpg
    >>> hm.info['key'] = 'value'
    >>> pbclient.update_helpingmaterial(hm)

**Note**: Categories actions POST, PUT and DELETE are only authorized to
admin users.

On queries and performance
--------------------------
There are two different approaches to perform queries with a pagination.

The first one is to use an offset and limit::

    >>> projects = pbclient.get_projects(limit=2, offset=2)
    # skips first two projects and returns next two

    [pybossa.Project("project3", 3), pybossa.Project("project4", 4)]

This approach has the advantage of being more "natural" and high level, but it
does not use all the power of the PYBOSSA server software (queries will run
slower when the pagination and data sets are high).

But you can also use `keyset pagination <http://use-the-index-luke.com/no-offset>`_
to take advantage of it in the PYBOSSA API. This drastically increases performance
of the API queries, so it is **highly recommended** to follow this approach.

The only thing it requires is the id of the item from which we want to obtain the
results, that has to be passed in the `last_id` argument.
To obtain the same results as in the previous example::

    >>> projects_with_last_id = pbclient.get_projects(limit=2, last_id=2)
    # next two projects after the project with id=2

    [pybossa.Project("project3", 3), pybossa.Project("project4", 4)]

    >>> projects == projects_with_last_id
    True

Running the tests
-----------------

Install the develompment requirements::

    $ pip install -r requirements-dev.txt

Run the tests::

    $ nosetests
