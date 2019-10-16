"""
test_cli
~~~~~~~~

This module contains the tests for the articleone.cli module.
"""
import unittest

from articleone import cli


class StatusTestCase(unittest.TestCase):
    def test__init(self):
        """cli.Status: The cli.Status class should populate its 
        attributes when instantiated.
        """
        expected = [
            'Spam',
        ]
        
        status = cli.Status(*expected)
        actual = [
            status.title,
        ]
        
        self.assertEqual(expected, actual)