"""
test_common
~~~~~~~~~~~~~~~

This module contains the test for the articleone.common module.
"""
import unittest

from articleone import common as com


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


class DescriptorsTestCase(unittest.TestCase):
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


class MemberTestCase(unittest.TestCase):
    def test_init(self):
        """common.Member.__init__: The attributes of the class 
        should be populated with the given values when initialized. 
        """
        expected = ['Spam', 'Eggs', 'D']
        
        obj = com.Member(*expected)
        actual = [obj.last_name, obj.first_name, obj.party]
        
        self.assertEqual(expected, actual)
