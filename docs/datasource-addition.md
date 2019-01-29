# Datasource addition
The visualizer component also provides the possibility of addition of different datasources to be used by the act plugins.

## Steps

1. In *visualizer.cfg* add the plugin to the list of desired plugins:

### Example:

```
[general]
host = 0.0.0.0
port = 6001
plugins = my_new_visualizer
datasource = my_new_datasource
debug = True
retries = 5

[my_new_visualizer]
var1 = 
var2 = 
var3 = 

[my_new_datasource]
var1 = 
var2 = 
var3 =
```
In this tutorial, we will use MyNewDatasource to represent a new visualizer datasource.

2. Create a new if statement condition in the file *visualizer/service/api/__init__.py* that will recognize if the new datasource added is informed in the configuration file (*visualizer.cfg*). If this condition is true, then the necessary variables to execute the plugin needs to be informed in the *visualizer.cfg* file and computed in the *visualizer/service/api/__init__.py*.

### Example:

```
import ConfigParser

try:

[...]
    for datasource in datasources:

    [...]

    if 'my_new_datasource' == datasource:
        var1 = config.get('my_new_datasource', 'var1')
        var2 = config.get('my_new_datasource', 'var2')
        var3 = config.get('my_new_datasource', 'var3')

[...].
```

3. After all necessary variables are computed by the *visualizer/service/api/__init__.py* file, the active plugin is able to use this variables to connect with the datasource and deal with all necessary data that needs to be collected.