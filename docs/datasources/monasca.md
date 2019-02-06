# Monasca Datasource

## How does it works?

Uses [Monasca](http://monasca.io/) as Asperathos Datasource to collect metrics about a running application.

## Configuration

In order to correctly configure the Visualizer to execute the K8s-Grafana plugin using Monasca as datasource, modifications in the *visualizer.cfg* file are necessary. Following you can check an example of a configuration file that can be used to execute the K8s-Grafana plugin with Monasca as datasource.

### Configuration file example:

```
[general]
host = 0.0.0.0
port = 6002
plugins = k8s-grafana
datasources = monasca
debug = true
retries = 5

[k8s-grafana]
k8s_conf_path = /home/user/.kube/config
visualizer_type = k8s-grafana
visualizer_ip = 10.11.5.62

[monasca]
name = monasca
type = monasca-datasource
url = https://10.11.15.254:8070
access = proxy
basic_auth = no
auth_type = token
token  = gAAAAABcEAtUO1uy24lKhTGt04pg4tYYrBQbR-w6wyzfkejenPhkL73YdtBopQmTeRcd1o3zWPeRJ4dFD9IcOcfVWrgaaF7Kxntk2muE_YpBvu3LBL0JPGYdAaeW-xsKBSesbU1DrZO7N5jmyMfq92BEY_Dtq9D1tLo4sE1gqICGmWY819ThZJs
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
         "datasource_type":"monasca"
      },
      "env_vars":{  
         [...]
      }
   }
}
```
