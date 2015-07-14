.. pybossa-client documentation master file, created by
   sphinx-quickstart on Tue Oct 16 11:21:34 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pybossa-client's documentation!
==========================================

This small library will help you to create and manage your projects in
a `PyBossa server <http://pybossa.com>`_.

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

Create a project::

    pbclient.create_project('Name of the Project', 'shortname', 'Description')

Change the long description of a project::

    project = pbclient.find_project(short_name='flickrperson')
    project.long_description = open('longdesc.html').read()
    
    pbclient.update_project(project)

Create a new task::

    task_info = {
        'image': 'http://farm9.staticflickr.com/8146/7566819662_f2c74e77d8_m.jpg'
    }
    pbclient.create_task(project_id, task_info)

.. note::
    The Category methods POST, PUT and DELETE are only allowed to **PyBossa
    admin users**. If you are not an admin, you can only get the Category names

Module overview
---------------

.. automodule:: pbclient
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

