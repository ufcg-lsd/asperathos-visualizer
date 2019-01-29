# Plugin development
This is an important step to enjoy all flexibility and features that this framework provides.

## Steps

1. In *visualizer.cfg* add the plugin to the list of desired plugins:

### Example:

```
[general]
host = 0.0.0.0
port = 6001
plugins = my_new_visualizer
debug = True
retries = 5

[my_new_visualizer]
var1 = 
var2 = 
var3 = 
```
In this tutorial, we will use MyNewVisualizer to represent a new visualizer plugin.

2. Create a new if statement condition in the file *visualizer/service/api/__init__.py* that will recognize if the new plugin added is informed in the configuration file (*visualizer.cfg*). If this condition is true, then the necessary variables to execute the plugin needs to be informed in the *visualizer.cfg* file and computed in the *visualizer/service/api/__init__.py*.

### Example:

```
import ConfigParser

try:

[...]
    
    if 'my_new_visualizer' in plugins:
        var1 = config.get('my_new_visualizer', 'var1')
        var2 = config.get('my_new_visualizer', 'var2')
        var3 = config.get('my_new_visualizer', 'var3')

[...]
```

3. Create a new folder under *visualizer/plugins* with the desired plugin name and add *__init__.py*.
 
4. Write a new python class under *visualizer/plugins/mynewvisualizer*. This class must extend *visualizer.plugins.base* and implement only four methods: __init__, start_visualization, stop_visualization, get_visualizer_url.
		   
* **Example**:

	* ```
		class MyNewVisualizer:

    		def __init__(self, app_id, plugin_info, collect_period, retries=100):
        	# set things up
			   pass
        
    		def start_visualization(self):
        	# visualizing logic
        	   pass

              def stop_visualization(self):
              # stop the visualizing logic
                 pass

              def get_visualizer_url(self):
              # returns the visualizer url
                 pass

	  ```

5. Edit the VisualizerBuilder class adding a new condition to check the plugin name in the start_visualization. Instantiate the plugin in the conditional case.
* **Example**:
	* ```
		...
		elif plugin_name == "mynewvisualizer":
	            plugin = MyNewVisualizer(app_id, plugin_info, collect_period, retries=retries)
		...
		```
