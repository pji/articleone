"""
test_common
~~~~~~~~~~~~~~~

This module contains the test for the articleone.common module.
"""
import unittest

from json import loads
from json.decoder import JSONDecodeError

from lxml import etree

from articleone import common as com


# Test data utilities.
def build_args_list():
    """Build a list of arguments for generating members."""
    return [
        ['Spam', 'Eggs', 'Democrat',],
        ['Bacon', 'Baked Beans', 'Democrat',],
        ['Ham', 'Tomato', 'Independent',],
    ]


def build_test_xml():
    """Build XML for test data."""
    root = etree.Element('book')
    child1 = etree.SubElement(root, 'spam')
    child1.text = 'foo'
    child2 = etree.SubElement(root, 'eggs')
    child2.text = 'bar'
    child3 = etree.SubElement(root, 'bacon')
    child3.text = 'baz'
    return root

 
# Tests.
class ValChamberTestCase(unittest.TestCase):
    def test_valid(self):
        """common.val_chamber: Given a valid value, the function 
        should return it.
        """
        expected = 'Senate'
        actual = com.val_chamber(None, expected)
        self.assertEqual(expected, actual)
    
    def test_invalid(self):
        """common.val_chamber: Given an invalid value, the function 
        should raise a ValueError exception.
        """
        expected = ValueError
        
        value = 'spam'
        class Eggs:
            msg = '{}'
        obj = Eggs()
        
        with self.assertRaises(expected):
            _ = com.val_chamber(obj, value)
    
    def test_normalized(self):
        """common.val_chamber: Given a common alternative value for 
        a type, the function should return a normalized value.
        """
        expected = ['Senate', 'House']
        
        values = ['sen', 'rep']
        actual = [com.val_chamber(None, value) for value in values]
        
        self.assertEqual(expected, actual)


class ValPartyTestCase(unittest.TestCase):
    def test__val_party__valid(self):
        """common.val_party: Given a value, if the value is a valid 
        party identifier, the function should return it.
        """
        expected = 'D'
        actual = com.val_party(None, expected)
        self.assertEqual(expected, actual)
    
    def test__val_party__invalid(self):
        """common.val_party: Given a value, if the value is not a 
        valid party identifier, the function should raise a 
        ValueError exception.
        """
        expected = ValueError
        
        class Spam:
            msg = '{}'
        obj = Spam()
        value = 'eggs'
        
        with self.assertRaises(expected):
            actual = com.val_party(obj, value)


class ValStateTestCase(unittest.TestCase):
    def test__valid(self):
        """common.val_state: Given a valid state abbreviation, 
        the function should return that value.
        """
        expected = 'IL'
        actual = com.val_state(None, expected)
        self.assertEqual(expected, actual)
    
    def test__invalid(self):
        """common.val_states: Given and invalid state abbreviation, 
        the function should raise a ValueError exceptions.
        """
        expected = ValueError
        value = 'spam'
        class Eggs:
            msg = '{}'
        with self.assertRaises(expected):
            _ = com.val_state(Eggs(), value)


class DescriptorsTestCase(unittest.TestCase):
    def test__ValidChamber(self):
        """common.ValidChamber: If the given value is a valid type, 
        the descriptor should assign it to the protected value.
        """
        expected = 'Senate'
        
        class Spam:
            chamber = com.ValidChamber()
        obj = Spam()
        value = 'sen'
        obj.chamber = value
        actual = obj.chamber
        
        self.assertEqual(expected, actual)

    def test__ValidParty(self):
        """common.ValidParty: If the given value is a valid party 
        identifier, the descriptor should assign it to the protected 
        attribute.
        """
        expected = 'I'
        
        class Spam:
            party = com.ValidParty()
        obj = Spam()
        value = 'I'
        obj.party = value
        actual = obj.party
        
        self.assertEqual(expected, actual)
    
    def test__ValidState(self):
        """common.ValidState: If the given value is a valid state 
        postal abbreviation, the descriptor should assign it to 
        the protected value.
        """
        expected = 'IL'
        
        class Spam:
            state = com.ValidState()
        obj = Spam()
        obj.state = expected
        actual = obj.state
        
        self.assertEqual(expected, actual)


class MemberTestCase(unittest.TestCase):
    def test_init(self):
        """common.Member.__init__: The attributes of the class 
        should be populated with the given values when initialized. 
        """
        expected = ['Spam', 'Eggs', 'D', 'Senate', 'IL']
        
        obj = com.Member(*expected)
        actual = [
            obj.last_name, 
            obj.first_name, 
            obj.party, 
            obj.chamber, 
            obj.state,
        ]
        
        self.assertEqual(expected, actual)
    
    def test__eq__equal(self):
        """common.Member.__eq__: The function should return True 
        when comparing two common.Member objects with the same 
        attribute values.
        """
        obj1 = com.Member('Spam', 'Eggs', 'D', 'Senate', 'IL')
        obj2 = com.Member('Spam', 'Eggs', 'D', 'Senate', 'IL')
        self.assertTrue(obj1 == obj2)
    
    def test__eq__notEqual(self):
        """common.Member.__eq__: The function should return False 
        when comparing two common.Member objects with different 
        attribute values.
        """
        obj = com.Member('Spam', 'Eggs', 'D')
        others = [
            com.Member('Spam', 'Eggs', 'R'),
            com.Member('Spam', 'Bacon', 'D'),
            com.Member('Baked Beans', 'Eggs', 'D'),
            com.Member('Spam', 'Ham', 'I'),
            com.Member('Tomato', 'Eggs', 'I'),
            com.Member('Dick', 'Durbin', 'D'),
            com.Member('Bernie', 'Sanders', 'I'),
            com.Member('Spam', 'Eggs', 'D', 'House'),
            com.Member('Spam', 'Eggs', 'D', None, 'IL'),
        ]
        for other in others:
            self.assertFalse(obj == other)
    
    def test__eq__notMember(self):
        """common.Member.__eq__: The method should raise a 
        NotImplemented exception if asked to compare a 
        non-common.Member object.
        """
        expected = NotImplemented
        
        obj1 = com.Member('Spam', 'Eggs', 'D')
        obj2 = 3
        actual = obj1.__eq__(obj2)
        
        self.assertEqual(expected, actual)
    
    def test__ne__equal(self):
        """common.Member.__ne__: The method should return False 
        when comparing two common.Member objects with the same 
        attribute values.
        """
        obj1 = com.Member('Spam', 'Eggs', 'D')
        obj2 = com.Member('Spam', 'Eggs', 'D')
        self.assertFalse(obj1 != obj2)
    
    def test__repr(self):
        """common.Member.__repr__: The method should return a 
        string representation of the object suitable for 
        troubleshooting.
        """
        expected = "Member('Spam', 'Eggs', 'D', 'House', 'IL')"
        
        mbr = com.Member('Spam', 'Eggs', 'D', 'House', 'IL')
        actual = mbr.__repr__()
        
        self.assertEqual(expected, actual)
    
    # @unittest.skip
    def test__from_json(self):
        """common.Member.from_json: Given a dictionary of 
        information from the @unitedstates project, the 
        method should return an instance of common.Members.
        """
        expected = com.Member('Spam', 'Eggs', 'Democrat', 'Senate', 'IL')
        
        data = {
            'name': {
                'first': 'Eggs',
                'last': 'Spam',
                'official_full': 'Spam Eggs',
            },
            'terms': [
                {
                    'type': 'sen',
                    'start': '1995-01-04',
                    'end': '2001-01-03',
                    'state': 'IL',
                    'class': 1,
                    'party': 'Democrat',
                },
                {
                    'type': 'sen',
                    'start': '2001-01-04',
                    'end': '2007-01-03',
                    'state': 'IL',
                    'class': 1,
                    'party': 'Democrat',
                },
            ]
        }
        actual = com.Member.from_json(data)
        
        self.assertEqual(expected, actual)


class BuildMemberMatrix(unittest.TestCase):
    def test_valid(self):
        """common.build_member_matrix: Given a list of common.
        Member objects, return a list of rows suitable for 
        writing into a report.
        """
        expected = [[
            'Last Name',
            'First Name',
            'Party',
        ],]
        expected.extend(build_args_list())
        
        mem_list = [com.Member(*args) for args in build_args_list()]
        actual = com.build_member_matrix(mem_list)
        
        self.assertEqual(expected, actual)


class ParseJsonTestCase(unittest.TestCase):
    def test_valid(self):
        """common.parse_json: Given a string containing data 
        in JSON syntax, the function should return Python 
        native objects representing that data.
        """
        data = ('{'
                '   "first name": "Spam",'
                '   "last name": "Eggs",'
                '   "party": "D"'
                '}')
        expected = loads(data)
        actual = com.parse_json(data)
        self.assertEqual(expected, actual)
    
    def test_invalid(self):
        """common.parse_json: Given a string containing invalid 
        JSON, the function should raise an exception.
        """
        expected = JSONDecodeError
        data = ('{'
                "   'first name': 'Spam',"
                '   "last name": "Eggs",'
                '   "party": "D"'
                '}')
        with self.assertRaises(expected):
            _ = com.parse_json(data)


class ParseXmlTestCase(unittest.TestCase):
    def test_validXml(self):
        """common.parse_xml: Given a string containing XML, the 
        function should return an lxml.etree.Element representing 
        the XML in the string.
        """
        expected = build_test_xml()
        
        text = ('<book>'
                '   <spam>foo</spam>'
                '   <eggs>bar</eggs>'
                '   <bacon>baz</bacon>'
                '</book>')
        actual = com.parse_xml(text)
        
        # lxml.etree._Element does not define __eq__, so we have 
        # to manually compare the attributes of the _Elements.
        for a, b in zip(expected, actual):
            self.assertEqual(a.tag, b.tag)
            self.assertEqual(a.text, b.text)
    
    def test_invalidXml(self):
        """common.parse_xml: Given a string containing invalid 
        XML, the function should raise an exception.
        """
        expected = etree.XMLSyntaxError
        
        text = ('<book>'
                '   <spam>foo<spam>'
                '   <eggs>bar</eggs>'
                '   <bacon>baz</bacon>'
                '</book>')
        
        with self.assertRaises(expected):
            actual = com.parse_xml(text)
