# Constructor with plugin, visualizer, datasource

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

import time
import requests
import json

import kubernetes as kube

from visualizer.utils.datasources.datasource_base import Base
from visualizer.service import api

class InfluxDataSource(Base):

    def __init__(self, monitor_plugin, database_data, app_id):
        Base.__init__(self, app_id, api.influxdb_datasource_name, api.influxdb_datasource_type)
        # Compute necessary variables
        self.datasource_access = api.influxdb_datasource_access
        self.datasource_url = database_data['url']
        self.datasource_port = database_data['port']
        self.database_name = database_data['name']
        if(monitor_plugin == 'kubejobs'):
            self.dashboard_path = './visualizer/utils/templates/dashboard-job-influxdb-kubejobs.template'
        elif(monitor_plugin == 'vertical'):
            self.dashboard_path = './visualizer/utils/templates/dashboard-job-influxdb-vertical.template'
        self.image = 'grafana/grafana:5.4.2'

    def create_grafana_datasource(self, user, password, visualizer_ip, node_port):
       
        url = "http://%s:%s@%s:%d/api/datasources" % (user, password, visualizer_ip, node_port)

        data_ds = {
            "name": self.datasource_name,
            "type": self.datasource_type,
            "url":"http://%s:%d" % (self.datasource_url, self.datasource_port),
            "access": self.datasource_access,
            "database": self.database_name
        }

        data = json.dumps(data_ds)
        headers = {'content-type': 'application/json'}

        successful_request = True
        try:
            requests.post(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError:
            successful_request = False        
        return successful_request

    def create_grafana_dashboard(self, user, password, visualizer_ip, node_port):
    
        url = "http://%s:%s@%s:%s/api/dashboards/db" % (user, password, visualizer_ip, node_port)

        opened = open(self.dashboard_path)

        template = opened.read().replace("app_id", self.app_id)
        dashboard_data = json.loads(template)
        data = json.dumps(dashboard_data)

        headers = {'content-type': 'application/json'}

        successful_request = True
        try:
            requests.post(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError:
            successful_request = False

        return successful_request
        

    def delete_visualizer_resources(self, visualizer_type='grafana', namespace="default"):
    
        # load kubernetes config
        kube.config.load_kube_config(api.k8s_conf_path)

        CoreV1Api = kube.client.CoreV1Api()
        # Create generic ``V1DeleteOptions``
        delete = kube.client.V1DeleteOptions()

        name = "%s-%s" % (visualizer_type, self.app_id)

        # Deleting Pod
        print("Deleting %s Pod for job %s..." % (visualizer_type, self.app_id))
        CoreV1Api.delete_namespaced_pod(
            name=name, namespace=namespace, body=delete)

        # Deleting service
        print("Deleting %s Service for job %s" % (visualizer_type, self.app_id))
        CoreV1Api.delete_namespaced_service(
            name=name, namespace=namespace, body=delete)

        influxdb_name = "%s-%s" % (self.datasource_type, self.app_id)
        # Deleting Pod
        print("Deleting InfluxDB resources...")
        CoreV1Api.delete_namespaced_pod(
            name=influxdb_name, namespace=namespace, body=delete)

        # Deleting service
        CoreV1Api.delete_namespaced_service(
        name=influxdb_name, namespace=namespace, body=delete)