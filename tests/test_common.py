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
    
    def test__eq__equal(self):
        """common.Member.__eq__: The function should return True 
        when comparing two common.Member objects with the same 
        attribute values.
        """
        obj1 = com.Member('Spam', 'Eggs', 'D')
        obj2 = com.Member('Spam', 'Eggs', 'D')
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
        expected = "Member('Spam', 'Eggs', 'D')"
        
        mbr = com.Member('Spam', 'Eggs', 'D')
        actual = mbr.__repr__()
        
        self.assertEqual(expected, actual)
