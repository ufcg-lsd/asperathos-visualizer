# Copyright (c) 2018 UFCG-LSD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ConfigParser

try:
    # Conf reading
    config = ConfigParser.RawConfigParser()
    config.read('./visualizer.cfg')
    
    """ General configuration """
    address = config.get('general', 'host')
    port = config.getint('general', 'port')
    plugins = config.get('general', 'plugins').split(',')
    datasources = config.get('general', 'datasources').split(',')
    use_debug = config.get('general', 'debug')
    retries = config.getint('general', 'retries')


    """ Validate if really exists a section to listed plugins """
    for plugin in plugins:
        if plugin != '' and plugin not in config.sections():
            raise Exception("plugin '%s' section missing" % plugin)

    """ Grafana parameters """
    if 'k8s-grafana' in plugins:
        k8s_conf_path = config.get('k8s-grafana', 'k8s_conf_path')
        visualizer_type = config.get("k8s-grafana", "visualizer_type")
        visualizer_ip = config.get("k8s-grafana", "visualizer_ip")  

    for datasource in datasources: 

        """ Validate if really exists a section to the datasource """
        if datasource != '' and datasource not in config.sections():
            raise Exception("datasource '%s' section missing" % datasource)

        """ Monasca parameters """
        if 'monasca' == datasource:
            monasca_datasource_name = config.get("monasca", "name")
            monasca_datasource_type = config.get("monasca", "type")
            monasca_datasource_url = config.get("monasca", "url")
            monasca_datasource_access = config.get("monasca", "access")
            monasca_datasource_basic_auth = config.getboolean("monasca", "basic_auth")
            monasca_datasource_auth_type = config.get("monasca", "auth_type")
            monasca_datasource_token = config.get("monasca", "token")  
        
        """ InfluxDB parameters """
        if 'influxdb' == datasource:
            influxdb_datasource_name = config.get("influxdb", "name")
            influxdb_datasource_type = config.get("influxdb", "type")
            influxdb_datasource_url = config.get("influxdb", "url")
            influxdb_datasource_access = config.get("influxdb", "access")
            
except Exception as e:
    print "Error: %s" % e.message
    quit()
