# Copyright (c) 2019 UFCG-LSD.
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

import unittest
import pytest

from visualizer.plugins.builder import VisualizerBuilder
from visualizer.plugins.k8s_grafana.plugin import K8sGrafanaProgress

"""
Class that represents the tests of the Visualizer builder

"""


class TestBuilder(unittest.TestCase):

    """
    Set up Builder object
    """

    def setUp(self):
        self.builder = VisualizerBuilder()

    def tearDown(self):
        pass

    """
    Test if the correct instance of the plugin is being
    build.
    """
    @pytest.mark.skip(
        reason="Can only be executed with a real \
            kube-config cluster informed.")
    def test_builder(self):
        visualizer01 = self.builder.get_visualizer('0002', 'kubejobs', True,
                                                   'k8s-grafana', 'monasca',
                                                   'usr', 'psswrd')

        self.assertTrue(isinstance(visualizer01, K8sGrafanaProgress))

        with self.assertRaises(Exception):
            self.builder.get_visualizer('0002',
                                        'unidentified-plugin',
                                        True,
                                        'unidentified-\
                                            visualizer-plugin',
                                        'unidentified-monasca',
                                        'usr', 'psswrd')
