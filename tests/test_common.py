"""
test_common
~~~~~~~~~~~~~~~

This module contains the test for the articleone.common module.
"""
import unittest

from articleone import common as com


class MemberTestCase(unittest.TestCase):
    def test_init(self):
        """common.Member.__init__: The attributes of the class 
        should be populated with the given values when initialized. 
        """
        expected = ['Spam', 'Eggs']
        
        obj = com.Member(*expected)
        actual = [obj.last_name, obj.first_name]
        
        self.assertEqual(expected, actual)
