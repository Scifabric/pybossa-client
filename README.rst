.. image:: https://travis-ci.org/PyBossa/pybossa-client.png
   :target: https://travis-ci.org/#!/PyBossa/pybossa-client
.. image:: https://img.shields.io/pypi/v/pybossa-client.svg
   :target: https://pypi.python.org/pypi/pybossa-client
.. image:: https://img.shields.io/pypi/dm/pybossa-client.svg
   :target: https://pypi.python.org/pypi/pybossa-client

Dead simple Python client for PyBossa
=====================================

Makes it easy to work with `PyBossa <http://pybossa.com>`_

Install
-------

You can install pybossa-client using **pip**, preferably while working in a 
`virtualenv <http://www.virtualenv.org/en/latest/index.html>`_::

    $ pip install pybossa-client 

Usage
-----

Setup::

    import pbclient

    # setup the server connection
    pbclient.set('endpoint', 'http://pybossa.com')
    pbclient.set('api_key', '--your-api-key-here--')

Create an project::

    pbclient.create_project('Name of the Project', 'shortname', 'Description')

Change the long description of a project::

    project = pbclient.find_project(short_name='flickrperson')[0]
    project.long_description = open('longdesc.html').read()
    
    pbclient.update_project(project)

Replace the task presenter template::

    project = pbclient.find_project(short_name='flickrperson')[0]
    project.info['task_presenter'] = open('presenter.html').read()
    
    pbclient.update_project(project)

Create a new task::

    task_info = {
        'image': 'http://farm9.staticflickr.com/8146/7566819662_f2c74e77d8_m.jpg'
    }
    pbclient.create_task(project_id, task_info)

**Note**: Categories actions POST, PUT and DELETE are only authorized to
admin users.

Running the tests
-----------------

Install the develompment requirements::

    $ pip install -r requirements-dev.txt

Run the tests::

    $ nosetests
