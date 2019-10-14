"""
test_model.py
~~~~~~~~~~~~~

This module contains the unit tests for the articleone.model module.
"""
import abc
import inspect
import unittest

from articleone import model


class BaseDescriptorTests(unittest.TestCase):
    """Unit tests for model.BaseDescriptor."""
    bd_count = 0
    
    def test_BaseDescriptor(self):
        """model._BaseDescriptor: A class named BaseDescriptor exists 
        in the model module and can me instantiated.
        """
        names = [item[0] for item in inspect.getmembers(model)]
        self.assertTrue('_BaseDescriptor' in names)
    
    def test_init(self):
        """model._BaseDescriptor.__init__: On initialization the 
        class should populate the storage_name attribute with 
        the expected name and increment the class's counter of 
        initializations.
        """
        counter = model._BaseDescriptor._counter
        expected_c = counter + 1
        expected_sn = f'__BaseDescriptor#{counter}'
        
        descr = model._BaseDescriptor()
        actual_c = model._BaseDescriptor._counter
        actual_sn = descr.storage_name
        
        self.assertEqual(expected_c, actual_c)
        self.assertEqual(expected_sn, actual_sn)
    
    def test_set(self):
        """model._BaseDescriptor.__set__: The descriptor should set
        the value of its attribute to the given value.
        """
        expected = 'spam'
        
        counter = model._BaseDescriptor._counter
        class Eggs:
            attr = model._BaseDescriptor()
        obj = Eggs()
        obj.attr = expected
        actual = obj.__dict__[f'__BaseDescriptor#{counter}']
                
        self.assertEqual(expected, actual)
    
    def test_get__instance(self):
        """model._BaseDescriptor.__get__: When called on an instance 
        of the protected class, the descriptor should return the 
        protected value.
        """
        expected = 'spam'
        
        counter = model._BaseDescriptor._counter
        class Eggs:
            attr = model._BaseDescriptor()
        obj = Eggs()
        obj.attr = expected
        actual = obj.attr
        
        self.assertEqual(expected, actual)

    def test_get__class(self):
        """model._BaseDescriptor.__get__: When called the 
        protected class should return the instance of the 
        descriptor.
        """
        expected = model._BaseDescriptor()
        
        class Eggs:
            attr = expected
        actual = Eggs.attr
        
        self.assertEqual(expected, actual)


class ValidatedTestCase(unittest.TestCase):
    def test_parent(self):
        """model.Validated: The class should be a subclass of 
        model._BaseDescriptor and abc.ABC.
        """
        self.assertTrue(issubclass(model.Validated, abc.ABC))
        self.assertTrue(issubclass(model.Validated, model._BaseDescriptor))
    
    def test_validate(self):
        """model.Validated.validate: Subclasses of the descriptor 
        should be required to define the validate() method.
        """
        expected = TypeError
        
        with self.assertRaises(expected):
            class Spam(model.Validated):
                pass
            obj = Spam()
    
    def test_set(self):
        """model.Validated.__set__: The descriptor should send 
        the given value to validate before setting the protected 
        attribute.
        """
        expected = ValueError
        
        class Descr(model.Validated):
            def validate(self, value):
                if not isinstance(value, bool):
                    raise ValueError('Bad.')
                return value
        class Spam:
            attr = Descr()
        obj = Spam()
        
        with self.assertRaises(expected):
            obj.attr = 1
    

class valfactoryTestCase(unittest.TestCase):
    def test_valfactory__subclass(self):
        """model.valfactory: Given a validation function and a 
        message, the function should return a model.Validator 
        subclass that uses the given values.
        """
        expected = model.Validated
        
        name = 'Eggs'
        def validate(self, value):
            return value
        msg = 'Bad value'
        actual = model.valfactory(name, validate, msg)
        
        self.assertTrue(issubclass(actual, expected))
    
    def test_valfactory__instantiate(self):
        """model.valfactory: Classes created by the factory 
        must be able to be instantiated.
        """
        expected_name = 'Eggs'
        expected_msg = 'Bad value'
        
        def validate(self, value):
            return value
        cls = model.valfactory(expected_name, validate, expected_msg)
        descr = cls()
        actual_name = cls.__name__
        actual_msg = descr.msg
        
        self.assertTrue(isinstance(descr, cls))
        self.assertTrue(isinstance(descr, model.Validated))
        self.assertEqual(expected_name, actual_name)
        self.assertEqual(expected_msg, actual_msg)
    
    def test_valfactory__validate(self):
        """model.valfactory: Classes created by the factory 
        validate the data as expected.
        """
        expected = 'eggs'
        expected_exc = ValueError
        
        name = 'Eggs'
        def validate(self, value):
            if value != expected:
                raise ValueError(self.msg)
            return value
        msg = f'Not {expected}.'
        Eggs = model.valfactory(name, validate, msg)
        class Bacon:
            attr = Eggs()
        obj = Bacon()
        obj.attr = 'eggs'
        actual = obj.attr
        
        self.assertEqual(expected, actual)
        with self.assertRaises(expected_exc):
            obj.attr = 'spam'


class TrustedTestCase(unittest.TestCase):
    def test__rename(self):
        """model.trusted: The decorator should change the 
        storage_name attribute of the given subclass of 
        model.Validated to the expected value.
        """
        expected = '_Spam__attr'
        
        def validate(self, value):
            return value
        Spam = model.valfactory('Spam', validate, 'Bad.')
        class Eggs:
            attr = Spam()
        cls = model.trusted(Eggs)
        actual = Eggs.attr.storage_name
        
        self.assertEqual(expected, actual)