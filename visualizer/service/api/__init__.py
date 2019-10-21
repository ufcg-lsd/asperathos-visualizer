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

import configparser
import kubernetes as kube

from visualizer.utils import logger

logger.configure_logging()
CONFIG_PATH = "./data/conf"
API_LOG = logger.Log('api', 'api.log')

try:
    # Conf reading
    config = configparser.RawConfigParser()
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

        # Setting default value
        k8s_conf_path = CONFIG_PATH

        # If explicitly stated in the cfg file, overwrite the variable
        if(config.has_section('k8s-grafana')):
            if(config.has_option('k8s-grafana', 'k8s_conf_path')):
                k8s_conf_path = config.get('k8s-grafana', 'k8s_conf_path')
            if(config.has_option('k8s-grafana', 'visualizer_ip')):
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
            monasca_datasource_basic_auth = config.getboolean(
                "monasca", "basic_auth")
            monasca_datasource_auth_type = config.get("monasca", "auth_type")
            monasca_datasource_token = config.get("monasca", "token")

        """ InfluxDB parameters """
        if 'influxdb' == datasource:
            influxdb_datasource_name = config.get("influxdb", "name")
            influxdb_datasource_type = config.get("influxdb", "type")
            influxdb_datasource_access = config.get("influxdb", "access")

except Exception as e:
    API_LOG.log("Error: %s" % e)
    quit()

""" Gets the IP address of one a the node contained
    in a Kubernetes cluster

    Raises:
        Exception -- It was not possible to connect with the
        Kubernetes cluster.

    Returns:
        string -- The node IP
"""


def get_node_cluster(k8s_conf_path):
    try:
        kube.config.load_kube_config(k8s_conf_path)
        CoreV1Api = kube.client.CoreV1Api()
        for node in CoreV1Api.list_node().items:
            is_ready = [s for s in node.status.
                        conditions if s.type == 'Ready'][0].status == 'True'
            if is_ready:
                node_info = node
        node_ip = node_info.status.addresses[0].address
        return node_ip
    except Exception:
        API_LOG.log(
            "Connection with the cluster %s was not successful" %
            k8s_conf_path)
