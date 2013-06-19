.. image:: https://travis-ci.org/PyBossa/pybossa-client.png
   :target: https://travis-ci.org/#!/PyBossa/pybossa-client

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

Create an application::

    pbclient.create_app('Name of the App', 'shortname', 'Description')

Change the long description of an app::

    app = pbclient.find_app(short_name='flickrperson')[0]
    app.long_description = open('longdesc.html').read()
    
    pbclient.update_app(app)

Replace the task presenter template::

    app = pbclient.find_app(short_name='flickrperson')[0]
    app.info['task_presenter'] = open('presenter.html').read()
    
    pbclient.update_app(app)

Create a new task::

    task_info = {
        'image': 'http://farm9.staticflickr.com/8146/7566819662_f2c74e77d8_m.jpg'
    }
    pbclient.create_task(app_id, task_info)

**Note**: Categories actions POST, PUT and DELETE are only authorized to
admin users.
