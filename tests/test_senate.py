"""
test_validators
~~~~~~~~~~~~~~~

This module contains the test for the articleone.senate module.
"""
import unittest

from lxml import etree

from articleone import common as com
from articleone import senate as sen

class SenatorTestCase(unittest.TestCase):
    def test__subclass(self):
        """senate.Senator: The class should be a subclass of 
        common.Member.
        """
        expected = com.Member
        actual = sen.Senator
        self.assertTrue(issubclass(actual, expected))
    
    # @unittest.skip
    def test__from_senate_xml(self):
        """senate.Senator.from_senate_xml: Given the details of 
        a senator as XML, the class should return an instance of 
        senate.Senator representing that senator.
        """
        expected = sen.Senator('Spam', 'Eggs', 'D')
        
        details = {
            'last_name': 'Spam',
            'first_name': 'Eggs',
            'party': 'D',
        }
        xml = build_senator_xml(details)
        actual = sen.Senator.from_xml(xml)
        
        self.assertEqual(expected, actual)


# Test data utilities.
def build_senator_xml(details):
    """Build the XML nodes used to create a new senate.Senator."""
    root = etree.Element('member')
    for detail in details:
        node = etree.SubElement(root, detail)
        node.text = details[detail]
    return root