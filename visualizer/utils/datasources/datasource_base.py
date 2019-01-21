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

class Base():

    def __init__(self, app_id, datasource_name, datasource_type):
        self.app_id = app_id
        self.datasource_name = datasource_name
        self.datasource_type = datasource_type
        
    def create_grafana_datasource(self, user, password, visualizer_ip, node_port):
        """Generates a influxdb datasource for grafana
        
        Arguments:
            user {string} -- Grafana's user with the necessary permissions
            password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of one of the slaves that will be used to access the visualizer
            node_port {int} -- Port where the visualizer will be running

        Returns:
            boolean -- The status of the request. 'True' with the request was successful, 'False' otherwise
        """

    def create_grafana_dashboard(self, user, password, visualizer_ip, node_port):
        """Generates a dashboard for grafana
        
        Arguments:
            user {string} -- Grafana's user with the necessary permissions
            password {string} -- Password of the Grafana user
            visualizer_ip {string} -- IP of one of the slaves that will be used to access the visualizer
            node_port {string} -- Port where the visualizer will be running
        
        Returns:
            boolean -- The status of the request. 'True' with the request was successful, 'False' otherwise
        """
        

    def delete_visualizer_resources(self, visualizer_type='grafana', namespace="default"):
        """Delete visualizer resources (Pod and Service) of a specific job
        
        Arguments:
            app_id {string} -- Id of the job launched
            visualizer_type {string} -- Type of the visualizer
            namespace {string} -- Namespace of the resources
        
        Returns:
            None
        """