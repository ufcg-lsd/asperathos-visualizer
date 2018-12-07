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
    visualizer = config.get('general', 'visualizer')
    datasource = config.get('general', 'datasource')
    use_debug = config.get('general', 'debug')
    retries = config.getint('general', 'retries')


    """ Validate if really exists a section to listed plugins """
    for plugin in plugins:
        if plugin != '' and plugin not in config.sections():
            raise Exception("plugin '%s' section missing" % plugin)

    if 'kubejobs' in plugins:
        k8s_conf_path = config.get('kubejobs', 'k8s_conf_path')
        count_queue = config.get('kubejobs', 'count_queue')
        redis_ip = config.get('kubejobs', 'redis_ip')

    """ Validate if really exists a section to the visualizer """
    if visualizer != '' and visualizer not in config.sections():
        raise Exception("visualizer '%s' section missing" % visualizer)

    """ Grafana parameters """
    if visualizer == 'grafana':
        visualizer_user = config.get("grafana", "user")
        visualizer_password = config.get("grafana", "password")
        visualizer_type = config.get("grafana", "visualizer_type")
        visualizer_ip = config.get("grafana", "visualizer_ip")  

    """ Validate if really exists a section to the datasource """
    if datasource != '' and datasource not in config.sections():
        raise Exception("datasource '%s' section missing" % datasource)
    
    """ Monasca parameters """
    if datasource == 'monasca':
        datasource_name = config.get("monasca", "name")
        datasource_type = config.get("monasca", "type")
        datasource_url = config.get("monasca", "url")
        datasource_access = config.get("monasca", "access")
        datasource_basic_auth = config.getboolean("monasca", "basic_auth")
        datasource_auth_type = config.get("monasca", "auth_type")
        datasource_token = config.get("monasca", "token")  

except Exception as e:
    print "Error: %s" % e.message
    quit()