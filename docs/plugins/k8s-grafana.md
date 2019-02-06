# K8s-Grafana Plugin

## How does it works?

Creates a Pod in a Kubernetes cluster that will give support to a [Grafana](https://grafana.com/) platform that will provide to the user a Visualization dashboard where can be checked the job progress.

## Configuration

In order to correctly configure the Visualizer to execute the K8s-Grafana plugin, modifications in the *visualizer.cfg* file are necessary. Following you can check an example of a configuration file that can be used to execute the K8s-Grafana plugin.

### Configuration file example:

```
[general]
host = 0.0.0.0
port = 6002
plugins = k8s-grafana
datasources = datasource
debug = true
retries = 5

[k8s-grafana]
# Path of the conf file of the Kubernetes cluster
k8s_conf_path = /home/user/.kube/config
visualizer_type = k8s-grafana

[datasource]
var1 =
var2 = 
var3 = 
```

## Execute plugin

In order to execute the plugin, a JSON needs to be correctly configurate with all necessary variables that will be used by Asperathos components. Following you can check an example of this JSON file that will be used to sends a POST request to the Asperathos Manager.

### JSON file example:

```javascript
{  
   "plugin":"plugin",
   "plugin_info":{  
      "username":"usr",
      "password":"psswrd",
      "cmd":[  
         [...]
      ],
      "img":"img",
      "init_size":1,
      "redis_workload":"workload",
      "config_id":"id",
      "control_plugin":"plugin",
      "control_parameters":{  
         [...]
      },
      "monitor_plugin":"plugin",
      "monitor_info":{  
         "expected_time":40
      },
      "enable_visualizer":true,
      "visualizer_plugin":"k8s-grafana",
      "visualizer_info":{  
         "datasource_type":"datasource"
      },
      "env_vars":{  
         [...]
      }
   }
}
```