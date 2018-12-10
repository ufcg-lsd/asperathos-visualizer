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

# from broker.plugins import base as plugin_base
from visualizer.service import api
from visualizer.utils.logger import Log
# from broker.utils.framework import authorizer
# from broker.utils.framework import optimizer
from visualizer import exceptions as ex
from visualizer.plugins.builder import VisualizerBuilder


API_LOG = Log("APIv10", "logs/APIv10.log")

visualized_apps = {}
builder = VisualizerBuilder()

def start_visualization(data, app_id):
    
    if 'plugin' not in data or 'plugin_info' not in data or 'visualizer' not in data or 'datasource' not in data: 
        API_LOG.log("Missing parameters in request")
        raise ex.BadRequestException()

    plugin = data['plugin']
    plugin_info = data['plugin_info']
    visualizer = data['visualizer']
    datasource = data['datasource']
   
    if app_id not in visualized_apps:
        executor = builder.get_visualizer(app_id, plugin, plugin_info, visualizer, datasource)
        visualized_apps[app_id] = executor
        executor.visualize_application()

    else:
        API_LOG.log("The application is already being visualized")
        raise ex.BadRequestException()

def visualizer_url(app_id):
    """Gets the URL to access the visualizer interface
    
    Arguments:
        app_id {string} -- Id of the job
    
    Returns:
        dict -- Key being 'url' and value being the visualizer URL access
    """

    if app_id not in visualized_apps.keys():
        API_LOG.log("Wrong request")
        raise ex.BadRequestException()

    visualizer_url = visualized_apps[app_id].get_application_visualizer_url()

    return {"url": visualizer_url}