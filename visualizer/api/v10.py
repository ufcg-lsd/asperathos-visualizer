# Copyright (c) 2018 LSD - UFCG.
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

from visualizer.utils import api as u
from visualizer.service.api import v10 as api


rest = u.Rest('v10', __name__)

""" Start the visualization of a running application.

    Normal response codes: 202
    Error response codes: 400
"""
@rest.post('/visualizing/<app_id>')
def start_visualization(data, app_id):
    return u.render(api.start_visualization(data, app_id))

""" Returns the url of the visualizer of the job.
                                                                              
    Normal response codes: 200
    Error response codes: 400
"""
@rest.get('/visualizing/<app_id>')
def get_visualizer_url(app_id):
    return u.render(api.visualizer_url(app_id))

""" Stop the visualization of a running application.

    Normal response codes: 202
    Error response codes: 400
"""
@rest.post('/visualizing/<app_id>/stop')
def stop_visualization(data, app_id):
    return u.render(api.stop_visualization(data, app_id))