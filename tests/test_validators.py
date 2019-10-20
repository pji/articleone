"""
test_validators
~~~~~~~~~~~~~~~

This module contains the test for the articleone.validators module.
"""
import unittest

from articleone import model
from articleone import validators as v


# Utility functions and classes.
class Descr:
    msg = '{}'


# Validator function test cases.
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


class ValHttpUrlTestCase(unittest.TestCase):
    def test_valid(self):
        """validators.val_http_url: Given a value, if the value is a 
        valid URL the function should return it.
        """
        expected = 'https://test.local:5000/test/path?key=value#frag'
        actual = v.val_http_url(None, expected)
        self.assertEqual(expected, actual)
    
    def test_invalidScheme(self):
        """validators.val_http_url: Given a value, if the value is 
        not a valid HTTP or HTTPS URL the function should raise a 
        ValueError exception.
        """
        expected = ValueError
        class Spam:
            msg = '{}'
        value = 'ftp://test.local'
        with self.assertRaises(expected):
            _ = v.val_http_url(Spam(), value)
    
    def test_normalizedConstruction(self):
        """validators.val_http_url: Given a value, if the value 
        contains any of the following the function should remove 
        them:
        
        * A parameter part delimiter with an empty parameter part 
        * A query part delimiter with an empty query part
        * A fragment part delimiter with an empty fragment part
        """
        expected = 'http://test.local/path'
        value = 'http://test.local/path;?#'
        actual = v.val_http_url(None, value)
        self.assertEqual(expected, actual)
    
    def test_normalizedEncoding(self):
        """validators.val_http_urlL Given a value, if the value 
        contains non-ASCII characters, the function should replace 
        them with their percent encoded value.
        """
        expected = 'http://t%C3%A9st.local/file%20path'
        value = 'http://tést.local/file%20path'
        actual = v.val_http_url(None, value)
        self.assertEqual(expected, actual)


class ValPhoneNumberTestCase(unittest.TestCase):
    def test_valid(self):
        """validators.val_phone_number: Given a value, if the 
        value is a valid North American Numbering Plan phone 
        number, the function should return it.
        """
        expected = '309-555-5555'
        actual = v.val_phone_number(Descr(), expected)
        self.assertEqual(expected, actual)
    
    def test_normalizeParens(self):
        """validators.val_phone_number: Given a value, if the 
        value contains an area code delimited by parentheses, 
        replace the delimiters with a hyphen.
        """
        expected = '309-555-5555'
        value = '(309)555-5555'
        actual = v.val_phone_number(Descr(), value)
        self.assertEqual(expected, actual)
    
    def test_normalNoDelim(self):
        """validators.val_phone_number: Given a value, if the 
        value is not hyphen delimited, the function should add 
        the hyphen delimiters and return the value.
        """
        expected = '309-555-5555'
        value = '3095555555'
        actual = v.val_phone_number(Descr(), value)
        self.assertEqual(expected, actual)
    
    def test_normalStr(self):
        """validators.val_phone_number: Given a value, if the 
        value is not a string, the function should coerce it 
        to a string.
        """
        expected = '309-555-5555'
        value = 3095555555
        actual = v.val_phone_number(Descr(), value)
        self.assertEqual(expected, actual)
    
    def test_invalid(self):
        """validators.val_phone_number: Given a value, if the 
        value is not a valid North American Numbering Plan phone 
        number, the function should raise a ValueError exception.
        """
        expected = ValueError
        value = 'spam'
        with self.assertRaises(expected):
            _ = v.val_phone_number(Descr(), value)


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


# Validating descriptors test cases.
class DescriptorsTestCase(unittest.TestCase):
    def test_HttpUrl(self):
        """validators.HttpUrl: The descriptor should validate and 
        normalize the given HTTP URL, and, if valid, assign it 
        to the protected attribute.
        """
        expected = 'http://test.local'
        
        class Spam:
            url = v.HttpUrl()
        obj = Spam()
        obj.url = expected
        actual = obj.url
        
        self.assertEqual(expected, actual)

    def test_Phone(self):
        """validators.Phone: Given a valid value, the descriptor 
        should normalize it and assign it to the protected 
        attribute.
        """
        expected = '309-555-5555'
        
        class Eggs:
            attr = v.Phone()
        obj = Eggs()
        obj.attr = expected
        actual = obj.attr
        
        self.assertEqual(expected, actual)
    
    
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
    
