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

import kubernetes as kube

from visualizer.plugins.base import Plugin
from visualizer.service import api
from visualizer.utils.datasources.datasource_influx import InfluxDataSource
from visualizer.utils.datasources.datasource_monasca import MonascaDataSource
from visualizer.utils.logger import Log

LOG_FILE = "k8s-grafana.log"
LOG_NAME = "k8s-grafana"
MONITORING_INTERVAL = 2


class K8sGrafanaProgress(Plugin):

    def __init__(self, app_id, monitor_plugin, enable_visualizer,
                 datasource_type, user, password, database_data, timeout=60):
        Plugin.__init__(self, app_id, enable_visualizer, timeout)
        # Compute necessary variables
        kube.config.load_kube_config(api.k8s_conf_path)
        self.LOG = Log(LOG_NAME, LOG_FILE)
        self.visualizer_url = "URL not generated!"
        self.datasource = datasource_type
        self.monitor_plugin = monitor_plugin
        self.enable_visualization = enable_visualizer
        self.app_id = app_id
        self.grafana_user = user
        self.grafana_password = password
        if datasource_type == 'influxdb':
            self.datasource = InfluxDataSource(
                monitor_plugin, database_data, app_id)
        elif datasource_type == 'monasca':
            self.datasource = MonascaDataSource(app_id)
        else:
            raise Exception("ERROR: Datasource type unknown...!")

        self.visualizer_type = api.visualizer_type

        # Gets the visualizer ip if the value is not explicitic in the config
        # file
        try:
            self.visualizer_ip = api.visualizer_ip
        except AttributeError:
            self.visualizer_ip = api.get_node_cluster(api.k8s_conf_path)

    def start_visualization(self):
        """ Starts the visualization of the job

        Arguments:
            None

        Returns:
            None
        """

        try:
            self._create_grafana_components(self.app_id,
                                            self.grafana_user,
                                            self.grafana_password,
                                            timeout=self.timeout)

        except Exception as e:
            self.LOG.log(e)

    def stop_visualization(self):
        """ Stop visualizer service and delete all resources

        Arguments:
            None
        Returns:
            None
        """
        self.LOG.log("The %s is stopping for %s..." % (type(self).__name__,
                                                       self.app_id))
        self.running = False
        self._delete_visualizer_resources()

    def get_visualizer_url(self):
        """ Gets the url to the visualizer of the specific job

        Arguments:
            None
        Returns:
          String -- The url of the visualizer
        """
        return self.visualizer_url

    def _delete_visualizer_resources(self, visualizer_type='grafana'):
        """Delete visualizer resources (Pod and Service) of a specific job

        Arguments:
            None or visualizer_type {string} -- Type of visualizer service
        Returns:
            None
        """
        self.datasource.delete_visualizer_resources(visualizer_type)

    def _get_grafana_pod_spec(self, grafana_port=3000):
        """ Create the Pod spec for grafana

        Arguments:
            grafana_port {int} -- Port that the grafana will serve

        Returns:
            Dict -- Dict with specs of grafana pod
        """
        grafana_pod_spec = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "grafana-%s" % self.app_id,
                "labels": {
                    "app": "grafana-%s" % self.app_id
                }
            },
            "spec": {
                "containers": [{
                    "name": "grafana-master",
                    "image": self.datasource.image,
                    "env": [{
                        "name": "MASTER",
                        "value": str(True)
                    }, {
                        "name": "GF_SECURITY_ADMIN_PASSWORD",
                        "value": self.grafana_password
                    }],
                    "ports": [{
                        "containerPort": grafana_port
                    }]
                }]
            }
        }

        return grafana_pod_spec

    def _get_grafana_service_spec(self, port=3000):
        """ Create the Service spec for grafana

        Arguments:
            grafana_port {int} -- Port that the grafana will serve

        Returns:
            Dict -- Dict with specs of grafana service
        """
        # Create the Service object for grafana
        visualizer_svc_spec = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "grafana-%s" % self.app_id,
                "labels": {
                    "app": "grafana-%s" % self.app_id
                }
            },
            "spec": {
                "ports": [{
                    "protocol": "TCP",
                    "port": port,
                    "targetPort": port
                }],
                "selector": {
                    "app": "grafana-%s" % self.app_id
                },
                "type": "NodePort"
            }
        }

        return visualizer_svc_spec

    def _create_grafana_pod(self, namespace='default'):
        """ Create the Pod for grafana

        Arguments:
            namespace {string} -- Namespace
            that the grafana pod will be created

        Returns:
            None
        """
        grafana_pod_spec = self._get_grafana_pod_spec()
        CoreV1Api = kube.client.CoreV1Api()
        try:
            self.LOG.log("Creating Grafana Pod...")
            CoreV1Api.create_namespaced_pod(
                namespace=namespace, body=grafana_pod_spec)
            self.LOG.log("Grafana Pod Created...!")
        except kube.client.rest.ApiException as e:
            self.LOG.log(e)

    def _create_grafana_service(self, namespace='default'):
        """ Create the Service for grafana

        Arguments:
            namespace {string} -- Namespace
            that the grafana service will be created

        Returns:
            None
        """
        grafana_svc_spec = self._get_grafana_service_spec()
        CoreV1Api = kube.client.CoreV1Api()
        node_port = None
        try:
            self.LOG.log("Creating Grafana Service...")
            s = CoreV1Api.create_namespaced_service(
                namespace=namespace, body=grafana_svc_spec)
            node_port = s.spec.ports[0].node_port
        except kube.client.rest.ApiException as e:
            self.LOG.log(e)
        return node_port

    def _create_datasource(self, grafana_user, grafana_password,
                           visualizer_ip, node_port, timeout):
        """ Create the Datasource in grafana

        Arguments:
            grafana_user {string} -- Grafana's
            user with the necessary permissions
            grafana_password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of one of
            the slaves that will be used to access the visualizer
            node_port {string} -- Port where the visualizer will be running
            timeout {int} -- Max time that will try create datasource

        Returns:
            Boolean -- State of creation of datasource
        """
        start = time.time()
        ready = False
        self.LOG.log("Trying Grafana on %s:%s..." % (visualizer_ip, node_port))
        while time.time() - start < timeout:
            time.sleep(5)
            datasource_result = self.datasource.create_grafana_datasource(
                grafana_user, grafana_password, visualizer_ip, node_port)
            if(datasource_result):
                self.LOG.log(
                    "Connected to Grafana on %s:%s!" %
                    (visualizer_ip, node_port))
                self.LOG.log("Data source created on Grafana")
                ready = True
                break
            else:
                self.LOG.log("Grafana is not ready yet!")
        return ready

    def _create_dashboard(self, grafana_user, grafana_password,
                          visualizer_ip, node_port, timeout):
        """ Create the Datasource in grafana

        Arguments:
            grafana_user {string} -- Grafana's
            user with the necessary permissions
            grafana_password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of oneof the
            slaves that will be used to access the visualizer
            node_port {string} -- Port where the visualizer will be running
            timeout {int} -- Max time that will try create dashboard

        Returns:
            Boolean -- State of creation of dashboard
        """
        start = time.time()
        ready = False
        self.LOG.log(
            "Trying to generate dashboard for Grafana on %s:%d..." %
            (visualizer_ip, node_port))
        while time.time() - start < timeout:
            time.sleep(5)
            dashboard_result = self.datasource.create_grafana_dashboard(
                grafana_user, grafana_password, visualizer_ip, node_port)
            if(dashboard_result):
                self.LOG.log(
                    "Dashboard of the job created on: http://%s:%s" %
                    (visualizer_ip, node_port))
                self.visualizer_url = "http://%s:%s" % (
                    visualizer_ip, node_port)
                ready = True
                break
            else:
                self.LOG.log("Grafana is not ready yet!")
        return ready

    def _create_grafana_components(self, app_id, grafana_user,
                                   grafana_password, namespace="default",
                                   visualizer_port=3000, timeout=60):
        """ Generates a individual visualizer dashboard for the Job.
        Create a Pod for the visualizer
        and expose it through a NodePort Service.

        Arguments:
            app_id {string} -- Id of the job launched
            img {string} -- Image grafana of the container
            namespace {string} -- pods's namespace
            visualizer_port {int} -- container's port
            timeout_id {int} -- timeout of the function

        Returns:
            tuple -- A pair with the ip and port running the grafana service
        """

        self._create_grafana_pod()
        node_port = self._create_grafana_service()

        visualizer_ip = self.visualizer_ip
        self.LOG.log(
            "Created Grafana on address: %s:%d" %
            (visualizer_ip, node_port))

        # Check when the visualizer is ready to create the datasource and
        # dashboard

        try:
            datasource_created = self._create_datasource(grafana_user,
                                                         grafana_password,
                                                         visualizer_ip,
                                                         node_port,
                                                         timeout)

            dashboard_created = self._create_dashboard(grafana_user,
                                                       grafana_password,
                                                       visualizer_ip,
                                                       node_port,
                                                       timeout)

            if datasource_created and dashboard_created:
                return visualizer_ip, node_port

            else:
                raise Exception("Could not provision Grafana!")

        except Exception:
            self.LOG.log("Timed out waiting for Grafana to be available.")
            self.LOG.log("Grafana address: %s:%d" % (visualizer_ip, node_port))
            self.datasource.delete_visualizer_resources(app_id)
