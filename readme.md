# Dead simple Python client for PyBossa

Makes it easy to work with [PyBossa](http://pybossa.com).

## Install

You can install pybossa-client using **pip**, preferably while working in a [virtualenv](http://www.virtualenv.org/en/latest/index.html):

```bash
pip install https://github.com/PyBossa/pybossa-client/zipball/master 
```

## Usage:

Setup:

```python
import pbclient

# setup the server connection
pbclient.set('endpoint', 'http://pybossa.com')
pbclient.set('api_key', '--your-api-key-here--')
```

Change the long description of an app:

```python
app = pbclient.find_app(short_name='flickrperson')
app.long_description = open('longdesc.html').read()

pbclient.update_app(app)
```

Create a new task

```python
task_info = {
    'image': 'http://farm9.staticflickr.com/8146/7566819662_f2c74e77d8_m.jpg'
}
pbclient.create_task(app_id, task_info)
```

