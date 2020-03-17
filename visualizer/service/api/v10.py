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

from visualizer.utils.logger import Log
from visualizer import exceptions
from visualizer.service import plugin_service


API_LOG = Log("APIv10", "logs/APIv10.log")

visualized_apps = {}


def start_visualization(data, app_id):
    """Starts the visualization of a job

    Arguments:
        app_id {string} -- Id of the job

    Returns:
        None
    """

    if 'plugin' not in data or 'enable_visualizer' not in data or \
            'visualizer_plugin' not in data or 'datasource_type' not in data:

        API_LOG.log("Missing parameters in request")
        raise exceptions.BadRequestException()

    plugin_name = data['plugin']
    enable_visualizer = data['enable_visualizer']
    visualizer_plugin = data['visualizer_plugin']
    datasource_type = data['datasource_type']
    user = data['username']
    password = data['password']
    theme = data.get('theme', 'light')

    if app_id not in visualized_apps:
        plugin = plugin_service.get_plugin(visualizer_plugin)
        if 'database_data' in data:
            database_data = data['database_data']
            executor = plugin(app_id, plugin_name,
                              enable_visualizer,
                              datasource_type, user,
                              password, database_data,
                              theme)

        else:
            executor = plugin(app_id, plugin_name,
                              enable_visualizer,
                              visualizer_plugin,
                              datasource_type,
                              user, password, theme)

        visualized_apps[app_id] = executor
        executor.start_visualization()

    else:
        API_LOG.log("The application is already being visualized")
        raise exceptions.BadRequestException()


def stop_visualization(data, app_id):
    """Stop the visualization of a job

    Arguments:
        app_id {string} -- Id of the job

    Returns:
        Plugin {Object} -- Returns a executor represeting the plugin executed
    """

    if ('enable_auth' in data.keys() and data['enable_auth']):
        if 'username' not in data or 'password' not in data:
            API_LOG.log("Missing parameters in request")
            raise exceptions.BadRequestException()

        # Commented because the authorization service not exists yet.
        # username = data['username']
        # password = data['password']

        # authorization = authorizer.get_authorization(api.authorization_url,
        #                                              username, password)

        # if not authorization['success']:
        #     API_LOG.log("Unauthorized request")
        #     raise exceptions.UnauthorizedException()

    if app_id not in visualized_apps.keys():
        raise exceptions.BadRequestException()

    if 'plugin' not in data\
        or 'visualizer_plugin' not in data\
            or 'datasource_type' not in data:

        API_LOG.log("Missing parameters in request")
        raise exceptions.BadRequestException()

    plugin = data['plugin']
    if plugin == 'kubejobs' or plugin == 'kubejobs_cost':
        # Call the executor by app_id and stop the visualization.
        visualized_apps[app_id].stop_visualization()

        return visualized_apps[app_id]


def visualizer_url(app_id):
    """Gets the URL to access the visualizer interface

    Arguments:
        app_id {string} -- Id of the job

    Returns:
        dict -- Key being 'url' and value being the visualizer URL access
    """

    if app_id not in visualized_apps.keys():
        API_LOG.log("Wrong request")
        raise exceptions.BadRequestException()
    try:
        url = visualized_apps[app_id].get_visualizer_url()
    except Exception as ex:
        API_LOG.log(ex)
    return {"url": url}


def install_plugin(source, plugin):
    status = plugin_service.install_plugin(source, plugin)
    if status:
        return {"message": "Plugin installed successfully"}, 200
    return {"message": "Error installing plugin"}, 400
