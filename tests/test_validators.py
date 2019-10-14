"""
test_validators
~~~~~~~~~~~~~~~

This module contains the test for the articleone.validators module.
"""
import unittest

from articleone import model
from articleone import validators as v


class ValTextTestCase(unittest.TestCase):
    def test__val_text__valid(self):
        """validators.val_text: If the given value is a valid string, 
        the function should return it.
        """
        expected = 'spam'
        actual = v.val_text(None, expected)
        self.assertEqual(expected, actual)
    
    def test__val_text__strCoersion(self):
        """validators.val_text: Given values that can be converted 
        to strings should be converted and returned.
        """
        expected = '100'
        actual = v.val_text(None, 100)
        self.assertEqual(expected, actual)
    
    # @unittest.skip
    def test_val_text__charsetNormalization(self):
        """validators.val.text: Given values should be normalized to 
        UTF-8 strings and returned, if the source character set is 
        given.
        """
        expected = 'résumé'
        b = b'r\xe9sum\xe9'
        actual = v.val_text(None, b, 'iso_8859_1')
        self.assertEqual(expected, actual)
    
    # @unittest.skip
    def test__val_text__invalidUtf8(self):
        """validators.val_text: If the given value contains invalid 
        characters for the expected character set, the value should 
        be rejected.
        """
        expected = ValueError
        
        class Spam:
            msg = 'Bad ({}).'
        obj = Spam()
        text = b'r\xc3sum\xc3'
        
        with self.assertRaises(ValueError):
            actual = v.val_text(obj, text)
    
    def test__val_text__normalization(self):
        """validators.val_text: If the given value contains unicode 
        characters that haven't been normalized, normalize them. The 
        default normal form should be NFC.
        """
        expected = 'á'
        text = '\u0061\u0301'
        actual = v.val_text(None, text)
        self.assertEqual(expected, actual)


class ValWhitelist(unittest.TestCase):
    def test__val_whitelist__valid(self):
        """validators.val_whitelist: Given a whitelist and a 
        value, if the value is in the whitelist it is valid, 
        and the function should return it.
        """
        expected = 'spam'
        
        whitelist = ['spam', 'eggs', 'bacon']
        value = 'spam'
        actual = v.val_whitelist(None, value, whitelist)
        
        self.assertEqual(expected, actual)
    
    def test__val_whitelist__invalid(self):
        """validators.val_whitelist: Given a whitelist and a 
        value, if the value is not in the whitelist it is invalid, 
        and the function should raise a ValueError exception.
        """
        expected = ValueError
        
        class Spam:
            msg = '{}'
        obj = Spam()
        value = 'baked beans'
        whitelist = ['spam', 'eggs', 'bacon']
        
        with self.assertRaises(expected):
            actual = v.val_whitelist(obj, value, whitelist)


class DescriptorsTestCase(unittest.TestCase):
    def test_Text(self):
        """validators.Text: The descriptor should normalize the 
        given value to a string and, if valid, assign it to the 
        protected attribute.
        """
        expected = 'spam'
        
        class Eggs:
            attr = v.Text()
        obj = Eggs()
        obj.attr = expected
        actual = obj.attr
        
        self.assertEqual(expected, actual) 