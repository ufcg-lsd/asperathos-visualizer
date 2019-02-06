# Copyright (c) 2017 UFCG-LSD.
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

from visualizer import exceptions as ex
from visualizer.service import api
from visualizer.plugins.k8s_grafana.plugin import K8sGrafanaProgress

""" Generates a visualizer builder of different types of visualizer.
    This class selects the type of visualizer that will be launched
    according with the user choice.
"""
class VisualizerBuilder:

    def __init__(self):
        pass

    def get_visualizer(self, app_id, plugin, enable_visualizer, 
    visualizer, datasource, user, password, database_data={}):
        """ Gets the visualizer executor of the job
        
        Arguments:
            app_id {string} -- Id of the job launched
            plugin {string} -- Plugin of the environment where the visualizer will be launched
            enable_visualizer {boolean} -- Flag that enables the visualization
            visualizer {int} -- Visualizer type that will be launched
            datasource {int} -- Datasource type of the visualizer launched
        
        Returns:
            Plugin -- Returns an object that represents a executions of a plugin
        """

        executor = None
        if plugin == "kubejobs" or plugin == "external_api":
            if visualizer == "k8s-grafana":
                executor = K8sGrafanaProgress(app_id, plugin, enable_visualizer, datasource, user, password, database_data)
        else:
            raise ex.BadRequestException()

        return executor
