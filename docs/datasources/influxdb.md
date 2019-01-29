# InfluxDB Datasource

## How does it works?

Creates a pod that will support a InfluDB database that will be used to collect all necessary metrics of the application.

## Configuration

In order to correctly configure the Visualizer to execute the K8s-Grafana plugin using InfluxDB as datasource, modifications in the *visualizer.cfg* file are necessary. Following you can check an example of a configuration file that can be used to execute the K8s-Grafana with InfluxDB as datasource.

### Configuration file example:

```
[general]
host = 0.0.0.0
port = 6002
plugins = k8s-grafana
datasources = influxdb
debug = true
retries = 5

[k8s-grafana]
k8s_conf_path = /home/user/.kube/config
visualizer_type = k8s-grafana
visualizer_ip = 10.11.5.62

[influxdb]
# Name of the datasource
name = InfluxDB
# Type of the datasource
type = influxdb
# URL of one of the nodes contained in the cluster
url = https://10.11.5.62
# The way of access
access = proxy
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
         "datasource_type":"influxdb"
      },
      "env_vars":{  
         [...]
      }
   }
}
```
