.. pybossa-client documentation master file, created by
   sphinx-quickstart on Tue Oct 16 11:21:34 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pybossa-client's documentation!
==========================================

This small library will help you to create and manage your applications in
a `PyBossa server <http://pybossa.com>`_.

Install
-------

You can install pybossa-client using **pip**, preferably while working in a 
`virtualenv <http://www.virtualenv.org/en/latest/index.html>`_::

    $ pip install https://github.com/PyBossa/pybossa-client/zipball/master 

Usage
-----

Setup::

    import pbclient

    # setup the server connection
    pbclient.set('endpoint', 'http://pybossa.com')
    pbclient.set('api_key', '--your-api-key-here--')

Create an application::

    pbclient.create_app('Name of the App', 'shortname', 'Description')

Change the long description of an app::

    app = pbclient.find_app(short_name='flickrperson')
    app.long_description = open('longdesc.html').read()
    
    pbclient.update_app(app)

Create a new task::

    task_info = {
        'image': 'http://farm9.staticflickr.com/8146/7566819662_f2c74e77d8_m.jpg'
    }
    pbclient.create_task(app_id, task_info)

Module overview
---------------

.. automodule:: pbclient
    :members:
   pybossa-client


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

