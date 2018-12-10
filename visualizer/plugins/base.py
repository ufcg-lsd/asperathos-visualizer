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

import threading
import time

# Plugins must extend Thread to facilitate each parallel plugin execution
class Plugin(threading.Thread):

    def __init__(self, app_id, info_plugin, timeout=60):
        threading.Thread.__init__(self)

        # Contains all the specific information for each plugin
        self.info_plugin = info_plugin

        # Flag that enable or disable the monitoring logic execution
        self.running = False

        # Dimensions is composed by default only application_id, but for each
        # plugin it can change and it is possible to add some relevant
        # information
        self.dimensions = {'application_id': app_id}

        # Time that visualize_application must be re executing until
        # something break into the execution
        self.timeout = timeout

        # The identifier for the submitted application
        self.app_id = app_id

    def stop(self):
        print "The %s is stopping for %s..." % (type(self).__name__,
                                                self.app_id)
        self.running = False

    # This method must be subscribed by each plugin that
    # extends this base class
    def visualize_application(self):
        pass