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
import pytest
import json
from unittest import TestCase
from requests_mock import Mocker
from visualizer.tests import fixtures
from visualizer.utils.datasources.datasource_influx import InfluxDataSource

tmp_file = fixtures.tmp_file


@pytest.mark.usefixtures("tmp_file")
class TestInfluxDataSource(TestCase):

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        monitor_plugin = 'kubejobs'
        database_data = {
            "url": "http://localhost/",
            "port": 12345,
            "name": "test"
        }
        app_id = "1"
        self.influx = InfluxDataSource(monitor_plugin, database_data, app_id)

    def test_create_grafana_datasource(self):
        user = "test"
        password = "test123"
        visualizer_ip = "192.168.1.90"
        node_port = 54321

        with Mocker() as m:
            m.post("http://%s:%s@%s:%d/api/datasources" % (user,
                                                           password,
                                                           visualizer_ip,
                                                           node_port))

            result = self.influx.create_grafana_datasource(user,
                                                           password,
                                                           visualizer_ip,
                                                           node_port)
            self.assertTrue(result)
            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 1)

    def test_create_grafana_dashboard(self):
        user = "test"
        password = "test123"
        visualizer_ip = "192.168.1.90"
        node_port = 54321

        template = {
            "test": "test"
            }

        self.tmp_file.write_text(json.dumps(template).decode('utf-8'))
        self.influx.dashboard_path = str(self.tmp_file.resolve())

        with Mocker() as m:

            m.post("http://%s:%s@%s:%s/api/dashboards/db" % (user,
                                                             password,
                                                             visualizer_ip,
                                                             node_port))

            result = self.influx.create_grafana_dashboard(user,
                                                          password,
                                                          visualizer_ip,
                                                          node_port)
            self.assertTrue(result)
            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 1)
            self.assertEquals(m.last_request.json(), template)
