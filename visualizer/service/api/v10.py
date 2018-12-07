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


API_LOG = Log("APIv10", "logs/APIv10.log")

submissions = {}

def submission_log(submission_id):
    pass
    # if submission_id not in submissions.keys():
    #     API_LOG.log("Wrong request")
    #     raise ex.BadRequestException()

    # logs = {'execution':'', 'stderr':'', 'stdout': ''}

    # exec_log = open("logs/apps/%s/execution" % submission_id, "r")
    # stderr = open("logs/apps/%s/stderr" % submission_id, "r")
    # stdout = open("logs/apps/%s/stdout" % submission_id, "r")

    # remove_newline = lambda x: x.replace("\n","")
    # logs['execution'] = map(remove_newline, exec_log.readlines())
    # logs['stderr'] = map(remove_newline, stderr.readlines())
    # logs['stdout'] = map(remove_newline, stdout.readlines())

    # exec_log.close()
    # stderr.close()
    # stdout.close()

    # return logs

def visualizer_url(submission_id):
    pass
    # """Gets the URL to access the visualizer interface
    
    # Arguments:
    #     submission_id {string} -- Id of the job
    
    # Returns:
    #     string -- The visualizer URL access
    # """

    # if submission_id not in submissions.keys():
    #     API_LOG.log("Wrong request")
    #     raise ex.BadRequestException()

    # visualizer_url = submissions[submission_id].get_application_visualizer_url()

    # return visualizer_url