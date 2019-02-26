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

from visualizer.plugins.base import Plugin

"""
Class that represents the tests of the base plugin for a visualizer
"""

class TestBase(unittest.TestCase):

    """
    Set up Base Plugin object
    """ 
    def setUp(self):
        self.base01 = Plugin('0001', True)
        self.base02 = Plugin('0002', False, 30)

    def tearDown(self):
        pass

    """
    Test the constructor for the base plugin
    """
    def testInit(self):

        self.assertTrue(self.base01.enable_visualizer)
        self.assertFalse(self.base02.enable_visualizer)

        self.assertFalse(self.base01.running)
        self.assertFalse(self.base02.running)

        dimensions01 = {'application_id': '0001'}
        self.assertTrue(self.base01.dimensions == dimensions01)

        dimensions02 = {'application_id': '0002'}
        self.assertTrue(self.base02.dimensions == dimensions02)

        self.assertTrue(self.base01.timeout == 60)
        self.assertTrue(self.base02.timeout == 30)

        self.assertTrue(self.base01.app_id == '0001')
        self.assertTrue(self.base02.app_id == '0002')
