# Config example

## visualizer.cfg: 
```
[general]
host = 0.0.0.0
port = 5002
plugins = plugin1
datasources = datasource1
debug = True
retries = 5

[plugin1]
k8s_conf_path = /home/user/.kube/config
visualizer_type = plugin1
visualizer_ip = 127.0.0.1

[datasource1]
name = datasource1_name
type = datasource1_type
url = http(s)?://<url>:<port>
access = proxy
datasource1_datasource_user = grafana_user
datasource1_datasource_password = grafana_password
# Just if need authentication #
basic_auth = no
auth_type = token
token = AAAAAABBBBCCCCCCC
```
