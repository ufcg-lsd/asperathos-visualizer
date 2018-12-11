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

from visualizer.service import api
from visualizer.plugins.base import Plugin

LOG_FILE = "progress.log"
TIME_PROGRESS_FILE = "time_progress.log"
MONITORING_INTERVAL = 2

class K8sGrafanaProgress(Plugin):

    def __init__(self, app_id, enable_visualizer, datasource, timeout=60):
        Plugin.__init__(self, app_id, enable_visualizer, timeout)

        self.visualizer_url = "URL not generated!"
        self.datasource = datasource
        self.enable_visualization = enable_visualizer

    def visualize_application(self):
        """ Starts the visualization of the job
        
        Arguments: 
            None
        
        Returns:
            None
        """
        if self.enable_visualization:
            self.visualizer_url = self.create_visualizer_components(self.app_id)

    def create_visualizer_components(self, app_id):
        """ Create all necessaries components (Pod and Service) to generates the visualizer of the job.
        
        Arguments:
            app_id {string} -- Id of the job launched

        Returns:
            string -- The visualizer url of the job
        """

        if(self.datasource == 'monasca'):
            visualizer_ip, node_port = self.create_grafana_components(app_id, timeout=self.timeout)
            visualizer_url = "http://%s:%d" % (visualizer_ip, node_port)
            return visualizer_url

    def create_grafana_components(self, app_id, img="monasca/grafana", namespace="default", visualizer_port=3000, timeout=60):
        """ Generates a individual visualizer dashboard for the Job.
        Create a Pod for the visualizer and expose it through a NodePort Service.
        
        Arguments:
            app_id {string} -- Id of the job launched
            img {string} -- Image grafana of the container
            namespace {string} -- pods's namespace
            visualizer_port {int} -- container's port
            timeout_id {int} -- timeout of the function
        
        Returns:
            tuple -- A pair with the ip and port running the grafana service
        """

        kube.config.load_kube_config(api.k8s_conf_path)

        # Compute necessary variables
        visualizer_user = api.visualizer_user
        visualizer_password = api.visualizer_password
        visualizer_type = api.visualizer_type
        visualizer_ip = api.visualizer_ip # FIXME(rafael): get node ip from k8s api instead of config

        # Create the Pod object for redis
        grafana_pod_spec = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "%s-%s" % (visualizer_type, app_id),
                "labels": {
                    "app": "%s-%s" % (visualizer_type, app_id)
                }
            },
            "spec": {
                "containers": [{
                    "name": "%s-master" % (visualizer_type),
                    "image": img,
                    "env": [{
                        "name": "MASTER",
                        "value": str(True)
                    }],
                    "ports": [{
                        "containerPort": visualizer_port
                    }]
                }]
            }
        }

        # Create the Service object for grafana
        visualizer_svc_spec = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name":"%s-%s" % (visualizer_type, app_id),
                "labels": {
                    "app": "%s-%s" % (visualizer_type, app_id)
                }
            },
            "spec": {
                "ports": [{
                    "protocol": "TCP",
                    "port": 3000,
                    "targetPort": 3000
                }],
                "selector": {
                    "app": "%s-%s" % (visualizer_type, app_id)
                },
                "type": "NodePort"
            }
        }

        # Create Service
        CoreV1Api = kube.client.CoreV1Api()
        node_port = None
        try:
            print("Creating %s Pod..." % (visualizer_type))
            CoreV1Api.create_namespaced_pod(
                namespace=namespace, body=grafana_pod_spec)
            print("Creating %s Service..." % (visualizer_type))
            s = CoreV1Api.create_namespaced_service(
                namespace=namespace, body=visualizer_svc_spec)
            node_port = s.spec.ports[0].node_port
        except kube.client.rest.ApiException as e:
            print(e)

        print("Created %s on address: %s:%d" % (visualizer_type, visualizer_ip, node_port))

        # Check when the visualizer is ready to create the datasource and dashboard
        visualizer_ready = False
        start = time.time()
        while time.time() - start < timeout:
            time.sleep(5)
            print("Trying %s on %s:%s..." % (visualizer_type, visualizer_ip, node_port))
            datasource_request = self.create_grafana_datasource(visualizer_user, visualizer_password, visualizer_ip, node_port)
            if(datasource_request):
                print("Connected to %s on %s:%s!" % (visualizer_type, visualizer_ip, node_port))
                print("Data source %s created on %s" % (api.datasource_name, visualizer_type))
                while time.time() - start < timeout:
                    dashboard_request = self.create_grafana_dashboard(app_id, visualizer_user, visualizer_password, visualizer_ip, node_port)
                    print("Trying to generate dashboard for %s on %s:%d..." % (visualizer_type, visualizer_ip, node_port))
                    if(dashboard_request):
                        print("Dashboard of the job created on: http://%s:%s" % (visualizer_ip, node_port))
                        visualizer_ready = True
                        break
                    else:
                        print("%s is not ready yet!" % (visualizer_type))
                break
            else: 
                print("%s is not ready yet!" % (visualizer_type))

        if visualizer_ready:
            return visualizer_ip, node_port
        else:
            print("Timed out waiting for %s to be available." % (visualizer_type))
            print("%s address: %s:%d" % (visualizer_type, visualizer_ip, node_port))
            delete_visualizer_resources(app_id, visualizer_type)
            raise Exception("Could not provision %s!" % (visualizer_type))

    def create_grafana_datasource(self, user, password, visualizer_ip, node_port):
        """Generates a datasource for a grafana
        
        Arguments:
            user {string} -- Grafana's user with the necessary permissions
            password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of one of the slaves that will be used to access the visualizer
            node_port {string} -- Port where the visualizer will be running
        
        Returns:
            boolean -- The status of the request. 'True' with the request was successful, 'False' otherwise
        """

        if self.datasource == 'monasca':
            return self.create_monasca_datasource(user, password, visualizer_ip, node_port)

    def create_monasca_datasource(self, user, password, visualizer_ip, node_port):
        """Generates a monasca datasource for a grafana
        
        Arguments:
            user {string} -- Grafana's user with the necessary permissions
            password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of one of the slaves that will be used to access the visualizer
            node_port {string} -- Port where the visualizer will be running
        
        Returns:
            boolean -- The status of the request. 'True' with the request was successful, 'False' otherwise
        """


        # Compute necessary variables
        name = api.datasource_name
        type_ds = api.datasource_type
        url_ds = api.datasource_url
        access = api.datasource_access 
        basic_auth = api.datasource_basic_auth
        auth_type = api.datasource_auth_type
        token = api.datasource_token

        url = "http://%s:%s@%s:%s/api/datasources" % (user, password, visualizer_ip, node_port)

        data_ds = {
            "name":name,
            "type":type_ds,
            "url":url_ds,
            "access":access,
            "basicAuth":basic_auth,
            "jsonData": {
                "authType":auth_type,
                "token":token
            }
        }

        data = json.dumps(data_ds)
        headers = {'content-type': 'application/json'}

        successful_request = True
        try:
            requests.post(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError:
            successful_request = False

        return successful_request


    def create_grafana_dashboard(self, app_id, user, password, visualizer_ip, node_port):
        """Generates a dashboard for grafana
        
        Arguments:
            app_id {string} -- Id of the job launched
            user {string} -- Grafana's user with the necessary permissions
            password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of one of the slaves that will be used to access the visualizer
            node_port {string} -- Port where the visualizer will be running
        
        Returns:
            boolean -- The status of the request. 'True' with the request was successful, 'False' otherwise
        """

        url = "http://%s:%s@%s:%s/api/dashboards/db" % (user, password, visualizer_ip, node_port)

        f = open('./visualizer/utils/templates/dashboard-job.template')

        template = f.read().replace("app_id", app_id)
        dashboard_data = json.loads(template)
        data = json.dumps(dashboard_data)

        headers = {'content-type': 'application/json'}

        successful_request = True
        try:
            requests.post(url, data=data, headers=headers)
        except requests.exceptions.ConnectionError:
            successful_request = False

        return successful_request

    def delete_visualizer_resources(self, app_id, visualizer_type, namespace="default"):
        """Delete visualizer resources (Pod and Service) of a specific job
        
        Arguments:
            app_id {string} -- Id of the job launched
            visualizer_type {string} -- Type of the visualizer
            namespace {string} -- Namespace of the resources
        
        Returns:
            None
        """

        # load kubernetes config
        kube.config.load_kube_config(api.k8s_conf_path)

        CoreV1Api = kube.client.CoreV1Api()
        # Create generic ``V1DeleteOptions``
        delete = kube.client.V1DeleteOptions()

        name = "%s-%s" % (visualizer_type, app_id)

        # Deleting Pod
        print("Deleting %s Pod for job %s..." % (visualizer_type, app_id))
        CoreV1Api.delete_namespaced_pod(
            name=name, namespace=namespace, body=delete)

        # Deleting service
        print("Deleting %s Service for job %s" % (visualizer_type, app_id))
        CoreV1Api.delete_namespaced_service(
            name=name, namespace=namespace, body=delete)

    def get_application_visualizer_url(self):
        """ Gets the url to the visualizer of the specific job
        
        Arguments: None
        
        Returns:
            String -- The url of the visualizer
        """
        return self.visualizer_url 
