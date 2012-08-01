# Dead simple Python client for PyBossa

Makes it easy to work with [PyBossa](http://pybossa.com).

### Usage:

Setup:

```python
import pbclient

# setup the server connection
pbclient.set('api_url', 'http://pybossa.com')
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

