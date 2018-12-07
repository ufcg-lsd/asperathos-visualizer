# Copyright (c) 2017 LSD - UFCG.
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


""" Returns the url of the visualizer monitoring the job.
                                                                              
    Normal response codes: 200
    Error response codes: 400
"""
@rest.get('/submissions/<submission_id>/visualizer')
def get_visualizer_url(submission_id):
    return "URL!"
    #return u.render(api.visualizer_url(submission_id))