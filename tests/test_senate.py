"""
test_senate
~~~~~~~~~~~

This module contains the test for the articleone.senate module.
"""
import unittest
from unittest.mock import Mock, patch

from lxml import etree

from articleone import common as com
from articleone import senate as sen


# Seed data.
senators_args = [
        ('Sanders', 'Bernard', 'I'),
        ('Durbin', 'Dick', 'D'),
        ('Duckworth', 'Tammy', 'D'),
    ]


# Test data utilities.
def build_senate_xml(data:list):
    """Build the XML nodes to represent senate.xml."""
    root = etree.Element('contact_information')
    fields = [
        'last_name',
        'first_name',
        'party',
    ]
    for senator in data:
        details = {key: value for key, value in zip(fields, senator)}
        member = build_senator_xml(details)
        root.append(member)
    updated = etree.SubElement(root, 'last_updated')
    updated.text = 'Wednesday, June 5, 2019: 9:28 AM EST'
    return root

def build_senator_xml(details:dict):
    """Build the XML nodes used to create a new senate.Senator."""
    root = etree.Element('member')
    for detail in details:
        node = etree.SubElement(root, detail)
        node.text = details[detail]
    return root


# Mock functions.
mock__fetch = Mock()
mock__fetch_senate_xml = Mock()
mock__parse_xml = Mock(return_value=build_senate_xml(senators_args))


# Tests.
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


class GetSenatorsTestCase(unittest.TestCase):
    @patch('articleone.common.parse_xml', new=mock__parse_xml)
    def test__get_senators__noError(self):
        """senate.get_senators: The function should return the 
        list of current U.S. senators as a list of senate.Senator 
        objects.
        """
        expected = [sen.Senator(*args) for args in senators_args]
        actual = sen.get_senators()
        self.assertEqual(expected, actual)
    
